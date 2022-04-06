import { FC, useState } from 'react'

const tabs = [
  'Overview',
  'Collections',
  'Images',
  'Stories',
  'Exhibitions & Events',
] as const
type Tab = typeof tabs[number]

type Props = {
  selected: Tab
  nResults: {
    Collections: number
    Images: number
    Stories: number
    'Exhibitions & Events': number
  }
}

export function formatNumber(number: number): string {
  return number.toLocaleString('en-US')
}

const Tabs: FC<Props> = (props) => {
  const { nResults } = props
  const [selected, setSelected] = useState(props.selected)
  return (
    <ul className="divide-y divide-gray-400 xl:flex xl:divide-y-0 xl:divide-x">
      {tabs.map((tab) => {
        return (
          <li key={tab}>
            <button
              onClick={() => setSelected(tab)}
              name="tab"
              value={tab}
              className={`block w-full px-5 py-4 text-left xl:inline xl:h-full ${
                selected == tab ? 'bg-black text-white' : ''
              }`}
            >
              {tab} {tab in nResults ? ` (${formatNumber(nResults[tab])})` : ''}
            </button>
          </li>
        )
      })}
    </ul>
  )
}
export default Tabs
