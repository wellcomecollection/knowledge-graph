import { FC, useEffect, useState } from 'react'

type Props = {
  query?: string
}

const SearchBox: FC<Props> = (props) => {
  const [query, setQuery] = useState(props.query)
  const [tab, setTab] = useState('works')

  useEffect(() => {
    setQuery(props.query)
  }, [props.query])

  return (
    <form>
      <div className="bg-paper-3 px-3 py-4">
        <div className="flex">
          <button
            type="button"
            className={`${
              tab == 'works' ? 'bg-paper-1' : 'bg-paper-2'
            } border border-b-0 border-r-0 border-paper-2 px-3 py-2`}
            onClick={() => setTab('works')}
          >
            Works
          </button>
          <button
            type="button"
            className={`${
              tab == 'stories' ? 'bg-paper-1' : 'bg-paper-2'
            } border border-b-0 border-paper-2 px-3 py-2`}
            onClick={() => setTab('stories')}
          >
            Stories
          </button>
        </div>
        <div className="flex w-full">
          <input
            className="text-xl focus:outline-none h-12 flex-grow border-2 border-paper-2 pl-2 placeholder-gray-300"
            type="text"
            name="query"
            value={query}
            placeholder="What are you looking for?"
            onChange={(event) => setQuery(event.currentTarget.value)}
          />

        </div>
      </div>
    </form>
  )
}

export default SearchBox
