import { FC, useState } from 'react'
import { Search, X } from 'react-feather'

type Props = {
  searchTerms?: string
  index?: string
}
const SearchBox: FC<Props> = (props) => {
  const [searchTerms, setSearchTerms] = useState(props.searchTerms)
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerms(e.target.value)
  }

  return (
    <form
      className="block w-full"
      action={`/search${props.index ? `/${props.index}` : ''}`}
      method="GET"
    >
      <div className="mx-auto flex justify-between gap-1">
        <div className="relative flex w-full items-center border-2 border-black">
          <input
            className="w-full p-2 pr-8 text-lg focus:outline-none"
            type="text"
            name="query"
            value={searchTerms}
            placeholder="What are you looking for?"
            onChange={(event) => setSearchTerms(event.currentTarget.value)}
            required
          ></input>
          <button
            type="reset"
            className="absolute right-0 p-2"
            onClick={() => setSearchTerms('')}
          >
            <X className="w-5" />
          </button>
        </div>
        <button
          className={`${
            searchTerms ? 'bg-black text-white' : 'bg-gray-300 text-black'
          } px-3 text-center `}
          type="submit"
        >
          <Search />
        </button>
      </div>
    </form>
  )
}
export default SearchBox
