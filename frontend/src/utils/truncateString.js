export function truncateString(str, maxLength) {
  if (!str || typeof str !== "string") return "";
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength) + "...";
}

export function truncateAddress(address, front = 6, back = 4) {
  if (!address) return "";
  return `${address.slice(0, front)}...${address.slice(-back)}`;
}
