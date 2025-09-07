export function copyToClipboard(text) {
  if (navigator?.clipboard?.writeText && window.isSecureContext) {
    return navigator.clipboard.writeText(text);
  } else {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.select();

    try {
      document.execCommand('copy');
      console.log('Copied text (fallback)');
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
    } finally {
      document.body.removeChild(textArea);
    }

    return Promise.resolve();
  }
}
