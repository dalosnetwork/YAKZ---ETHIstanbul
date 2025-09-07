export const handleForwardLink = (url) => {
  const formattedUrl = url.startsWith("http://") || url.startsWith("https://") ? url : `https://${url}`;

  const newWindow = window.open(formattedUrl, "_blank", "noopener,noreferrer");
  if (newWindow) newWindow.opener = null;
};
