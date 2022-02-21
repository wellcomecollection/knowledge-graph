import { FC, ReactNode } from 'react'

import Head from 'next/head'

type Props = {
  children?: ReactNode
  debug?: boolean
  title: string
  description: string
}

const Layout: FC<Props> = ({ children, title, description, debug = false }) => {
  const emojiSVG = `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🔍</text></svg>`

  return (
    <div className="bg-offwhite-1 min-h-screen">
      <Head>
        <meta charSet="utf-8" />
        <title>{title}</title>
        <meta name="description" content={description} />
        <link rel="icon" href={emojiSVG} />
      </Head>
      <div
        className={`mx-auto mb-4 max-w-screen-md p-4 font-sans antialiased  ${
          debug ? 'debug' : ''
        }`}
      >
        {children}
      </div>
    </div>
  )
}
export default Layout
