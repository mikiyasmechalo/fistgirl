import sys
import re
import urllib.request
import urllib.error

def main():
    test_urls = [
        "https://fuckingfast.co/mkx39mgx8koc#PRAGMATA_Cracked_--_fitgirl-repacks.site_--_.part01.rar",
        "https://fuckingfast.co/akb08wunesaf#Ready_or_Not_--_fitgirl-repacks.site_--_.part01.rar"
    ]

    for ff_url in test_urls:
        m = re.search(r'fuckingfast\.co/(?:f/)?([a-zA-Z0-9]+)', ff_url)
        if not m:
            print("ERROR: Could not extract file ID from URL:", ff_url)
            continue

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

        try:
            req = urllib.request.Request(post_url, data=b"", headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                hx_redirect = resp.headers.get("hx-redirect") or resp.headers.get("HX-Redirect")
                if hx_redirect:
                    print("SUCCESS:", file_id, "->", hx_redirect.strip()[:60] + "...")
                else:
                    print("ERROR: No hx-redirect header found for", file_id)
        except urllib.error.HTTPError as e:
            hx_redirect = e.headers.get("hx-redirect") or e.headers.get("HX-Redirect")
            if hx_redirect:
                print("SUCCESS (from error headers):", file_id, "->", hx_redirect.strip()[:60] + "...")
            else:
                print(f"ERROR: HTTP {e.code} for {file_id}")
        except Exception as e:
            print(f"ERROR: {e} for {file_id}")

if __name__ == "__main__":
    main()
