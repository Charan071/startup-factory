export function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function truncateMiddle(value: string, visible = 18) {
  if (value.length <= visible) {
    return value;
  }

  const head = Math.ceil((visible - 3) / 2);
  const tail = Math.floor((visible - 3) / 2);
  return `${value.slice(0, head)}...${value.slice(-tail)}`;
}
