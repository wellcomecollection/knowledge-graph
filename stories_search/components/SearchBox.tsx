import { FC, useEffect, useState } from 'react'

type Props = {
  query?: string
}

const SearchBox: FC<Props> = (props) => {
  const [query, setQuery] = useState(props.query)

  useEffect(() => {
    setQuery(props.query)
  }, [props.query])

  return (
    <form>
      <div>
        <input
          type="text"
          name="query"
          value={query}
          placeholder="What are you looking for?"
          onChange={(event) => setQuery(event.currentTarget.value)}
        />
        <button aria-label="Search stories" type="submit">
          🔎
        </button>
      </div>
    </form>
  )
}

export default SearchBox
