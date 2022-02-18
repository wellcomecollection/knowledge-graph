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
        className={`mx-auto mb-4 max-w-screen-md p-4 font-sans antialiased ${
          debug ? 'debug' : ''
        }`}
      >
        {children}
      </div>
    </div>
  )
}
export default Layout
