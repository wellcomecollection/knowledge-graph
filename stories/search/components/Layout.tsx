import { FC, ReactNode } from 'react'

import Head from 'next/head'

type Props = {
  children?: ReactNode
  debug?: boolean
  title: string
  description: string
}

const Layout: FC<Props> = ({ children, title, description, debug = false }) => {
  return (
    <div>
      <Head>
        <meta charSet="utf-8" />
        <title>{title}</title>
        <meta name="description" content={description} />
      </Head>
      <div
        className={`antialiased p-4 font-sans max-w-screen-md mx-auto ${
          debug ? 'debug' : ''
        }`}
      >
        {children}
      </div>
    </div>
  )
}
export default Layout
