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
      <div className="flex w-full text-2xl">
        <input
          className="focus:outline-none h-12 flex-grow rounded-l-md border-2 border-r-0 border-gray-600 pl-2"
          type="text"
          name="query"
          value={query}
          placeholder="What are you looking for?"
          onChange={(event) => setQuery(event.currentTarget.value)}
        />
        <button
          className="h-12 w-16 rounded-r-md border-2 border-gray-600 bg-gray-300"
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
