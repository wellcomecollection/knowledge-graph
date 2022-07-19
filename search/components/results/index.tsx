export const formatDate = (date: Date): string => {
  return new Date(date).toLocaleDateString('en-GB', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

export function capitalise(input?: string) {
  return (input ? input : '').replace(/(^\w{1})|(\s+\w{1})/g, (letter) =>
    letter.toUpperCase()
  )
}
