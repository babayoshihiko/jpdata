import os
import posixpath
import zipfile
import warnings


# ------------------------------------------------------------
# UTF-8 byte-level filesystem helpers (bypass QGIS/PyQt)
# ------------------------------------------------------------


def make_dirs_utf8(path_str):
    if not path_str:
        return
    path_bytes = path_str.encode("utf-8", "surrogateescape")
    parts = path_bytes.split(b"/")
    current = b""
    for part in parts:
        if not part:
            continue
        current = current + b"/" + part
        try:
            os.mkdir(current)
        except FileExistsError:
            pass


def open_utf8(path_str, mode="wb"):
    path_bytes = path_str.encode("utf-8", "surrogateescape")
    fd = os.open(path_bytes, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o666)
    return os.fdopen(fd, mode)


# ------------------------------------------------------------
# Helper to detect ambiguous Shift-JIS backslash (0x5C)
# ------------------------------------------------------------


def warn_if_ambiguous(filename_original, decoded):
    """
    Warn if the original CP437-decoded string contains characters
    that map to 0x5C after CP932 decoding (backslash/Yen ambiguity).
    """
    if "\\" in filename_original:
        warnings.warn(
            f"[SJIS Warning] Possible ambiguous 0x5C in ZIP filename: {filename_original!r}"
        )

    # Warn if filename contains a Yen sign where Windows might confuse it
    if "¥" in decoded or "￥" in decoded:
        warnings.warn(
            f"[SJIS Notice] Filename contains Yen sign: {decoded!r}. "
            "This is safe, but ensure this is intentional."
        )


# ------------------------------------------------------------
# Main unzip function
# ------------------------------------------------------------


def unzip_qgis_safe(folder_path, zip_file):
    """
    Safely unzip inside QGIS without filename mojibake.
    Handles CP932, UTF-8, backslashes, Yen signs, and bypasses PyQt.
    """
    zip_path = posixpath.join(folder_path, zip_file)

    if not os.path.exists(zip_path):
        raise FileNotFoundError(zip_path)

    with zipfile.ZipFile(zip_path, "r") as zf:

        for zip_info in zf.infolist():

            # RAW original (already CP437-decoded by zipfile)
            filename_original = zip_info.filename

            # -------------------------------------------------
            # Step 1 — Decode correctly
            # -------------------------------------------------
            if (zip_info.flag_bits & (1 << 11)) != 0:
                # UTF-8 flag present (perfect)
                filename = filename_original
            else:
                # Decode correctly from Shift-JIS style ZIPs
                raw = filename_original.encode("cp437", "replace")
                try:
                    filename = raw.decode("cp932", "replace")
                except:
                    filename = filename_original  # fallback

            # -------------------------------------------------
            # Step 2 — Warn about ambiguous backslashes/Yen
            # -------------------------------------------------
            warn_if_ambiguous(filename_original, filename)

            # -------------------------------------------------
            # Step 3 — Normalise separators only
            # -------------------------------------------------
            filename = filename.translate(
                {
                    0x5C: ord("/"),  # "\"  → "/"
                    0xFF3C: ord("/"),  # "＼" → "/"
                }
            )
            # DO NOT touch ¥ (U+00A5) or ￥ (U+FFE5)

            # Build correct full path
            output_file_path = posixpath.join(folder_path, filename)

            # -------------------------------------------------
            # Step 4 — Create directories via UTF-8 bytes
            # -------------------------------------------------
            if zip_info.is_dir():
                make_dirs_utf8(output_file_path)
                continue

            parent_dir = posixpath.dirname(output_file_path)
            make_dirs_utf8(parent_dir)

            # -------------------------------------------------
            # Step 5 — Write file safely (UTF-8 bytes)
            # -------------------------------------------------
            with zf.open(zip_info) as src, open_utf8(output_file_path) as dst:
                dst.write(src.read())

    return True
