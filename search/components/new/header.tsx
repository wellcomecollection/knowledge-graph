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
    <div className="mx-auto px-5 py-8 md:w-4/5 md:px-12 xl:w-3/4">
      <header className="flex items-end justify-between">
        <img
          src="/images/logo.png"
          alt="Wellcome Collection"
          className="h-12"
        />
        <div className="flex items-center gap-8 text-lg">
          <Link href="/">
            <a className="hidden no-underline xl:inline">Plan your visit</a>
          </Link>
          <Link href="/">
            <a className="hidden no-underline xl:inline">
              Explore our collections
            </a>
          </Link>
          <Link href="/">
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
        <div className="flex w-full flex-col gap-y-8 py-10">
          <form className="block w-full">
            <SearchBox />
          </form>
          {isHomePage ? (
            <div>
              Looking to search our collections?{' '}
              <br className="block sm:hidden" />
              <a href="/collections">
                Go to our collections search
                <ArrowRight className="inline-block w-4" />
              </a>
            </div>
          ) : null}
        </div>
      ) : null}
      {menuSelected ? (
        <div className="py-10">
          <Menu />
        </div>
      ) : null}
    </div>
  )
}
export default Header
