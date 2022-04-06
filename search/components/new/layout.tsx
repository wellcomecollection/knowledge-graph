import { FC } from 'react'
import Header from './header'

type Props = {
  isHomePage?: boolean
}
const Layout: FC<Props> = ({ isHomePage, children }) => {
  return (
    <div className="w-full antialiased">
      <Header isHomePage={isHomePage} />
      <div className="mt-20 w-full">{children}</div>
    </div>
  )
}
export default Layout
