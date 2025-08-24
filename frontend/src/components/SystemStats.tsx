import React from 'react'
import type { MapGrid, Order } from '../types'
import { useBots } from '../hooks/userApi'
import robotUrl from '../assets/svg/robot.svg'

interface SystemStatsProps {
    gridData: MapGrid | null
    orders: Order[]
}

const SystemStats: React.FC<SystemStatsProps> = ({ gridData, orders }) => {
    if (!gridData) return null
    const bots = useBots()


    const stats = {
        totalBots: gridData.total_bots,
        activeBots: bots.data != null ? bots.data.filter(bot => bot.status === 'IDLE').length : 0,
        totalOrders: orders.length,
        pendingOrders: orders.filter(o => o.status === 'PENDING').length,
        activeOrders: orders.filter(o => ['ASSIGNED', 'PICKED_UP'].includes(o.status)).length,
        deliveredOrders: orders.filter(o => o.status === 'DELIVERED').length
    }

    const statCards = [
        {
        title: 'Active Bots',
        value: `${stats.activeBots}/${stats.totalBots}`,
        icon: robotUrl,
        color: 'from-blue-500 to-blue-600',
        textColor: 'text-blue-100',
        bgAccent: 'bg-blue-500/10',
        progress: (stats.activeBots / stats.totalBots) * 100
        },
        {
        title: 'Pending Orders',
        value: stats.pendingOrders,
        icon: '⏳',
        color: 'from-orange-500 to-orange-600',
        textColor: 'text-orange-100',
        bgAccent: 'bg-orange-500/10',
        urgent: stats.pendingOrders > 5
        },
        {
        title: 'In Progress',
        value: stats.activeOrders,
        icon: '🚀',
        color: 'from-green-500 to-green-600',
        textColor: 'text-green-100',
        bgAccent: 'bg-green-500/10'
        },
        {
        title: 'Delivered',
        value: stats.deliveredOrders,
        icon: '✅',
        color: 'from-purple-500 to-purple-600',
        textColor: 'text-purple-100',
        bgAccent: 'bg-purple-500/10'
        }
    ]

    return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 mb-6">
        <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <div className="w-2 h-6 bg-gradient-to-b from-blue-500 to-purple-600 rounded-full"></div>
            System Status
            </h3>
            <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-500">Live</span>
            </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
            {statCards.map((stat, index) => (
            <div
                key={index}
                className={`relative overflow-hidden rounded-xl bg-gradient-to-br ${stat.color} p-4 text-white transform transition-all duration-200 hover:scale-105 hover:shadow-lg ${
                stat.urgent ? 'animate-pulse ring-2 ring-red-400' : ''
                }`}
            >
                <div className="relative z-10">
                <div className="flex items-center justify-between mb-2">
                    {typeof stat.icon === 'string' && stat.icon.endsWith('.svg') ? (
                        <img src={stat.icon} alt="Robot" className="w-7 h-7" />
                    ) : (
                        <span className="text-2xl">{stat.icon}</span>
                    )}
                    {stat.progress && (
                    <div className="w-8 h-1 bg-white/30 rounded-full overflow-hidden">
                        <div 
                        className="h-full bg-white rounded-full transition-all duration-500"
                        style={{ width: `${stat.progress}%` }}
                        ></div>
                    </div>
                    )}
                </div>
                <div className={`text-sm font-medium ${stat.textColor} mb-1`}>
                    {stat.title}
                </div>
                <div className="text-2xl font-bold text-white">
                    {stat.value}
                </div>
                </div>
                <div className="absolute -top-4 -right-4 w-16 h-16 bg-white/10 rounded-full"></div>
                <div className="absolute -bottom-2 -left-2 w-8 h-8 bg-white/5 rounded-full"></div>
            </div>
            ))}
        </div>
        </div>
    )
}

export default SystemStats
