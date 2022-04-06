import { FC, useState } from 'react'
import { Search, X } from 'react-feather'

type Props = {
  query: string
}
const SearchBox: FC<Props> = (props) => {
  const [query, setQuery] = useState(props.query)

  return (
    <div className="mx-auto flex justify-between gap-1">
      <div className="flex w-full items-center border-2 border-black">
        <input
          className="focus:outline-none w-full p-2 text-lg"
          type="text"
          name="query"
          value={query}
          placeholder="What are you looking for?"
          onChange={(event) => setQuery(event.currentTarget.value)}
          required
        ></input>
        <button
          type="reset"
          className="flex items-center justify-center p-2"
          onClick={() => setQuery('')}
        >
          <X className="w-5" />
        </button>
      </div>
      <button
        className={`${
          query ? 'bg-black text-white' : 'bg-gray-300 text-black'
        } px-3 text-center `}
        type="submit"
      >
        <Search />
      </button>
    </div>
  )
}
export default SearchBox
