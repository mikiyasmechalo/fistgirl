import sys
import re
import urllib.request
import urllib.error

def get_direct_link(ff_url):
    # Extract file ID from URL like https://fuckingfast.co/mkx39mgx8koc#... or https://fuckingfast.co/f/mkx39mgx8koc
    m = re.search(r'fuckingfast\.co/(?:f/)?([a-zA-Z0-9]+)', ff_url)
    if not m:
        return None, f"Could not extract file ID from URL: {ff_url}"

    file_id = m.group(1)
    post_url = f"https://fuckingfast.co/f/{file_id}/go"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "HX-Request": "true",
        "HX-Current-URL": f"https://fuckingfast.co/{file_id}",
        "Origin": "https://fuckingfast.co",
        "Referer": f"https://fuckingfast.co/{file_id}",
    }

    # Attempt 1: Direct POST without cookies (fastest and bypasses Cloudflare GET challenge)
    try:
        req = urllib.request.Request(post_url, data=b"", headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=12) as resp:
            hx_redirect = resp.headers.get("hx-redirect") or resp.headers.get("HX-Redirect")
            if hx_redirect:
                return hx_redirect.strip(), None
    except urllib.error.HTTPError as e:
        hx_redirect = e.headers.get("hx-redirect") or e.headers.get("HX-Redirect")
        if hx_redirect:
            return hx_redirect.strip(), None
    except Exception:
        pass

    # Attempt 2: Fallback with cookie jar
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
        req = urllib.request.Request(post_url, data=b"", headers=headers, method="POST")
        with opener.open(req, timeout=12) as resp:
            hx_redirect = resp.headers.get("hx-redirect") or resp.headers.get("HX-Redirect")
            if hx_redirect:
                return hx_redirect.strip(), None
    except urllib.error.HTTPError as e:
        hx_redirect = e.headers.get("hx-redirect") or e.headers.get("HX-Redirect")
        if hx_redirect:
            return hx_redirect.strip(), None
    except Exception:
        pass

    return None, "No hx-redirect header returned from fuckingfast.co"

def main():
    if len(sys.argv) < 2:
        print("ERROR: No URL provided", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    direct_link, err = get_direct_link(url)
    if direct_link:
        print(direct_link)
        sys.exit(0)
    else:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
