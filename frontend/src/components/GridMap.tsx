import React from 'react'
import type { MapGrid, GridCell } from '../types'
import robotUrl from '../assets/svg/robot.svg'

interface GridMapProps {
    gridData: MapGrid | null
    selectedBot: number | null
    onCellClick: (x: number, y: number, cell: GridCell) => void
}

const GridMap: React.FC<GridMapProps> = ({ gridData, selectedBot, onCellClick }) => {
    if (!gridData) {
        return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
            <div className="flex items-center justify-center h-80">
            <div className="text-center">
                <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <span className="text-gray-600 font-medium">Loading map...</span>
            </div>
            </div>
        </div>
        )
    }

    const renderCell = (x: number, y: number) => {
        const cellKey = `${x},${y}`
        const cell = gridData.grid[cellKey]
        if (!cell) return null

        let cellClasses = 'w-12 h-12 border-2 border-gray-300 flex flex-col items-center justify-center cursor-pointer transition-all duration-200 hover:scale-110 hover:z-10 relative group text-xs font-bold'
        let cellContent = ''
        let bgColor = 'bg-gray-50 hover:bg-blue-100 hover:border-blue-400'
        let shadowClass = 'hover:shadow-lg'
        
        // Enhanced cell styling
        if (cell.is_restaurant) {
        const restaurantIcons: Record<string, string> = {
            RAMEN: '🍜',
            PIZZA: '🍕', 
            CURRY: '🍛',
            SUSHI: '🍣'
        }
        bgColor = 'bg-gradient-to-br from-yellow-200 to-orange-300 hover:from-yellow-300 hover:to-orange-400 border-yellow-400'
        cellContent = restaurantIcons[cell.restaurant_type || ''] || cell.restaurant_type?.[0] || 'R'
        shadowClass = 'shadow-md hover:shadow-xl'
        } else if (cell.is_delivery_point) {
        bgColor = 'bg-gradient-to-br from-green-200 to-emerald-300 hover:from-green-300 hover:to-emerald-400 border-green-400'
        cellContent = '🏠'
        shadowClass = 'shadow-md hover:shadow-xl'
        } else if (cell.is_bot_station) {
        bgColor = 'bg-gradient-to-br from-purple-200 to-violet-300 hover:from-purple-300 hover:to-violet-400 border-purple-400'
        cellContent = '⚡'
        shadowClass = 'shadow-md hover:shadow-xl'
        }

        // Bot styling with enhanced effects
        if (cell.bots && cell.bots.length > 0) {
        const bot = cell.bots[0]
        bgColor = 'bg-gradient-to-br from-blue-400 to-blue-600 hover:from-blue-500 hover:to-blue-700 border-blue-500 animate-pulse'
        cellContent = <img src={robotUrl} alt="Robot" className="w-6 h-6" />
        shadowClass = 'shadow-lg hover:shadow-2xl'
        
        if (selectedBot === bot?.id) {
            cellClasses += ' ring-4 ring-red-400 ring-opacity-75 scale-110 z-20'
            bgColor += ' ring-red-400'
        }
        }

        // Order indicators
        if (cell.active_orders && cell.active_orders.length > 0) {
        cellClasses += ' ring-2 ring-orange-500 ring-opacity-60'
        }

        return (
        <div
            key={cellKey}
            className={`${cellClasses} ${bgColor} ${shadowClass} rounded-lg`}
            onClick={() => onCellClick(x, y, cell)}
            title={`(${x},${y}) ${cell.name}`}
        >
            <div className="text-lg mb-1">{cellContent}</div>
            <div className="text-xs text-gray-700 font-medium bg-white/70 px-1 rounded">{x},{y}</div>
            
            {/* Tooltip */}
            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-30">
            {cell.name} ({x},{y})
            {cell.bots && cell.bots.length > 0 && (
                <div>Bot #{cell.bots[0]?.id} - {cell.bots[0]?.battery_level}% battery</div>
            )}
            </div>
        </div>
        )
    }

    return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <div className="w-2 h-6 bg-gradient-to-b from-green-500 to-blue-600 rounded-full"></div>
            Delivery Map
            </h3>
            <div className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
            9×9 Grid
            </div>
        </div>
        
        {/* Enhanced Grid Container */}
        <div className="relative">
            <div className="grid grid-cols-9 gap-2 p-4 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl border-2 border-gray-300">
            {Array.from({ length: 9 }, (_, y) =>
                Array.from({ length: 9 }, (_, x) => renderCell(x, y))
            )}
            </div>
            
            {/* Grid coordinates */}
            <div className="absolute -left-8 top-4 bottom-4 flex flex-col justify-around text-xs text-gray-500 font-medium">
            {Array.from({ length: 9 }, (_, i) => (
                <div key={i} className="flex items-center justify-center w-6 h-12">
                {i}
                </div>
            ))}
            </div>
            <div className="absolute -bottom-8 left-4 right-4 flex justify-around text-xs text-gray-500 font-medium">
            {Array.from({ length: 9 }, (_, i) => (
                <div key={i} className="flex items-center justify-center w-12 h-6">
                {i}
                </div>
            ))}
            </div>
        </div>
        
        <div className="mt-8 grid grid-cols-2 gap-4 text-sm">
            <div className="space-y-2">
            <div className="flex items-center gap-3 p-2 bg-blue-50 rounded-lg">
                <div className="w-6 h-6 bg-gradient-to-br from-blue-400 to-blue-600 rounded flex items-center justify-center">
                  <img src={robotUrl} alt="Robot" className="w-5 h-5" />
                </div>
                <span className="font-medium text-blue-800">Delivery Bot</span>
            </div>
            <div className="flex items-center gap-3 p-2 bg-green-50 rounded-lg">
                <div className="w-6 h-6 bg-gradient-to-br from-green-200 to-emerald-300 rounded flex items-center justify-center">🏠</div>
                <span className="font-medium text-green-800">Delivery Point</span>
            </div>
            </div>
            <div className="space-y-2">
            <div className="flex items-center gap-3 p-2 bg-yellow-50 rounded-lg">
                <div className="w-6 h-6 bg-gradient-to-br from-yellow-200 to-orange-300 rounded flex items-center justify-center">🍕</div>
                <span className="font-medium text-yellow-800">Restaurant</span>
            </div>
            <div className="flex items-center gap-3 p-2 bg-purple-50 rounded-lg">
                <div className="w-6 h-6 bg-gradient-to-br from-purple-200 to-violet-300 rounded flex items-center justify-center">⚡</div>
                <span className="font-medium text-purple-800">Bot Station</span>
            </div>
            </div>
        </div>
        
        {selectedBot && (
            <div className="mt-4 p-3 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
            <div className="flex items-center gap-2">
                <span className="text-blue-600">🎯</span>
                <span className="text-blue-800 font-medium">Bot #{selectedBot} selected - Click any empty cell to move</span>
            </div>
            </div>
        )}
        </div>
    )
}

export default GridMap
