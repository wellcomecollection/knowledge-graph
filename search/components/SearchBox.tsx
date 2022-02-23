import { FC, useEffect, useState } from 'react'

type Props = {
  query?: string
  index?: string
}

const SearchBox: FC<Props> = (props) => {
  const [query, setQuery] = useState(props.query)
  const [index, setIndex] = useState(props.index)

  useEffect(() => {
    setQuery(props.query)
  }, [props.query])
  useEffect(() => {
    setIndex(props.index)
  }, [props.index])

  const search = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (query) {
      window.location.href = `/?query=${query}&index=${index}`
    }
  }

  return (
    <form onSubmit={search}>
      <div className="bg-paper-3 px-3 py-4">
        <div className="flex">
          <button
            type="submit"
            className={`${
              index == 'works' ? 'bg-paper-1' : 'bg-paper-2'
            } border-2 border-b-0 border-r-0 border-paper-2 px-3 py-2`}
            onClick={() => setIndex('works')}
          >
            Works
          </button>
          <button
            type="submit"
            className={`${
              index == 'stories' ? 'bg-paper-1' : 'bg-paper-2'
            } border-2 border-b-0 border-l-0 border-paper-2 px-3 py-2`}
            onClick={() => setIndex('stories')}
          >
            Stories
          </button>
        </div>
        <div className="flex w-full">
          <input
            className="focus:outline-none h-12 flex-grow border-2 border-paper-2 pl-2 text-xl placeholder-gray-300"
            type="text"
            name="query"
            value={query}
            placeholder="What are you looking for?"
            onChange={(event) => setQuery(event.currentTarget.value)}
            required
          />
        </div>
      </div>
    </form>
  )
}

export default SearchBox
