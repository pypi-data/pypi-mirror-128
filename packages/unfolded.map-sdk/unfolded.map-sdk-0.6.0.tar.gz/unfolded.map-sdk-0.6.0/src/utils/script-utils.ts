/* global document */

// Ensure we only load a script once
const scriptLoadPromises: Record<string, Promise<void>> = {};

export function loadScript(url: string): Promise<void> {
  if (!scriptLoadPromises[url]) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    const head = document.querySelector('head');
    head?.appendChild(script);

    scriptLoadPromises[url] = new Promise(resolve => {
      // @ts-expect-error differing callback argument types
      script.onload = resolve;
    });
  }
  return scriptLoadPromises[url];
}
