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
      <div className="w-full flex text-2xl">
        <input
          className="pl-2 flex-grow h-12 rounded-l-md border-2 border-r-0 border-gray-600 focus:outline-none"
          type="text"
          name="query"
          value={query}
          placeholder="What are you looking for?"
          onChange={(event) => setQuery(event.currentTarget.value)}
        />
        <button
          className="h-12 w-16 rounded-r-md bg-gray-300 border-2 border-gray-600"
          aria-label="Search stories"
          type="submit"
        >
          🔎
        </button>
      </div>
    </form>
  )
}

export default SearchBox
