import { FC } from 'react'
import Header from './header'

type Props = {
  isHomePage?: boolean
}
const Layout: FC<Props> = ({ isHomePage, children }) => {
  return (
    <div className="relative antialiased">
      <div className="absolute z-40 w-full">
        <Header isHomePage={isHomePage} />
      </div>
      <div className="w-full space-y-8 pt-24 ">{children}</div>
    </div>
  )
}
export default Layout
