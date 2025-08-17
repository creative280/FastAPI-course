def getExtension(contentType):
    if contentType == "image/jpeg":
        return ".jpg"
    elif contentType == "image/png":
        return ".png"
    elif contentType == "image/gif":
        return ".gif"
    elif contentType == "image/webp":
        return ".webp"
    else:
        return "No"