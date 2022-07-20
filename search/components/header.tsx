import { ArrowRight, Menu as MenuIcon, Search, XCircle } from 'react-feather'
import { FC, useState } from 'react'

import Link from 'next/link'
import Menu from './menu'
import SearchBox from './search-box'

type Props = { isHomePage?: boolean }

const Header: FC<Props> = ({ isHomePage }) => {
  const [searchSelected, setSearchSelected] = useState(false)
  const [menuSelected, setMenuSelected] = useState(false)

  return (
    <div
      className={`bg-white ${
        searchSelected || menuSelected ? 'shadow-2xl' : null
      } ${menuSelected ? 'bg-red text-white' : 'bg-white'}`}
    >
      <div className="mx-auto py-6 px-5 lg:w-3/4">
        <header className="flex items-end justify-between">
          <Link href="/">
            <a>
              <img
                src="/images/logo.png"
                alt="Wellcome Collection"
                className={`h-10 ${menuSelected ? 'invert filter' : ''}`}
              />
            </a>
          </Link>
          <div className="flex items-center gap-8 text-lg">
            <Link href="/">
              <a className="hidden no-underline xl:inline">Plan your visit</a>
            </Link>
            <Link href="/search/works">
              <a className="hidden no-underline xl:inline">
                Explore our collections
              </a>
            </Link>
            <Link href={`/search/stories`}>
              <a className="hidden no-underline xl:inline">Read our stories</a>
            </Link>
            <button
              className="block"
              onClick={() => {
                setSearchSelected(!searchSelected)
                setMenuSelected(false)
              }}
            >
              {searchSelected ? <XCircle /> : <Search />}
            </button>
            <button
              className="block"
              onClick={() => {
                setMenuSelected(!menuSelected)
                setSearchSelected(false)
              }}
            >
              <div className="flex items-center justify-center gap-2">
                Menu
                {menuSelected ? <XCircle /> : <MenuIcon />}
              </div>
            </button>
          </div>
        </header>
        {searchSelected ? (
          <div className="flex w-full flex-col gap-y-8 pt-10">
            <SearchBox />

            {isHomePage ? (
              <div>
                Looking to search our collections?{' '}
                <br className="block sm:hidden" />
                <Link href="/search/works">
                  <a>
                    Go to our collections search
                    <ArrowRight className="inline-block w-4" />
                  </a>
                </Link>
              </div>
            ) : null}
          </div>
        ) : null}
        {menuSelected ? (
          <div className="pt-10">
            <Menu />
          </div>
        ) : null}
      </div>
    </div>
  )
}
export default Header
