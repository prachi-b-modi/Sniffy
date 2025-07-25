from overlay_agent import run as overlay_run

js_code = overlay_run(r"add glass-style sticky notes overlay")
print("\nGenerated JavaScript code:")
print("="*80)
print(js_code)
print("="*80)
print("\nYou can now inject this code via Stagehand / exa.ai / chrome.scripting")
