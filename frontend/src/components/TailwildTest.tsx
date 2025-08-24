import React from 'react'

/**
 * Tailwind Sanity Test Component
 * Проверяет паддинги, маргины, размеры, цвета, шрифты, flex/grid.
 */
const TailwindTest: React.FC = () => {
  return (
    <div className="p-10 space-y-8">
      {/* Background / padding / margin test */}
      <div className="p-6 m-4 bg-red-500 text-white rounded-xl shadow-lg hover:bg-green-500">
        Padding 6 / Margin 4 / Red background → hover Green
      </div>

      {/* Size + border + typography */}
      <div className="w-64 h-32 border-4 border-dashed border-blue-500 flex items-center justify-center text-xl font-bold">
        w-64 h-32 border-4 text-xl bold
      </div>

      {/* Flexbox */}
      <div className="flex gap-4 p-4 bg-gray-100">
        <div className="flex-1 bg-blue-200 p-4 text-center">flex-1</div>
        <div className="flex-1 bg-blue-400 p-4 text-center">flex-1</div>
        <div className="flex-1 bg-blue-600 p-4 text-center text-white">flex-1</div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-3 gap-4 p-4 bg-gray-100">
        <div className="bg-purple-200 p-4 text-center">1</div>
        <div className="bg-purple-400 p-4 text-center">2</div>
        <div className="bg-purple-600 p-4 text-center text-white">3</div>
      </div>

      {/* Arbitrary values (JIT check) */}
      <div className="w-[150px] h-[75px] bg-[magenta] text-white flex items-center justify-center">
        w-[150px] h-[75px] bg-[magenta]
      </div>
    </div>
  )
}

export default TailwindTest
