import React from 'react'
import type { Order } from '../types'

interface OrderListProps {
    orders: Order[]
}

const OrderList: React.FC<OrderListProps> = ({ orders }) => {
    const getStatusConfig = (status: string) => {
        switch (status) {
        case 'PENDING': 
            return { 
            color: 'bg-orange-500', 
            icon: '⏳', 
            text: 'text-orange-700',
            bg: 'bg-orange-50 border-orange-200'
            }
        case 'ASSIGNED': 
            return { 
            color: 'bg-blue-500', 
            icon: '🔄', 
            text: 'text-blue-700',
            bg: 'bg-blue-50 border-blue-200'
            }
        case 'PICKED_UP': 
            return { 
            color: 'bg-purple-500', 
            icon: '📦', 
            text: 'text-purple-700',
            bg: 'bg-purple-50 border-purple-200'
            }
        case 'DELIVERED': 
            return { 
            color: 'bg-green-500', 
            icon: '✅', 
            text: 'text-green-700',
            bg: 'bg-green-50 border-green-200'
            }
        case 'CANCELLED': 
            return { 
            color: 'bg-red-500', 
            icon: '❌', 
            text: 'text-red-700',
            bg: 'bg-red-50 border-red-200'
            }
        default: 
            return { 
            color: 'bg-gray-500', 
            icon: '❓', 
            text: 'text-gray-700',
            bg: 'bg-gray-50 border-gray-200'
            }
        }
    }

    const restaurantIcons: Record<string, string> = {
        RAMEN: '🍜',
        PIZZA: '🍕', 
        CURRY: '🍛',
        SUSHI: '🍣'
    }

    return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <div className="w-2 h-6 bg-gradient-to-b from-purple-500 to-pink-600 rounded-full"></div>
            Orders
            </h3>
            <div className="bg-gray-100 px-3 py-1 rounded-full">
            <span className="text-sm font-semibold text-gray-700">{orders.length}</span>
            </div>
        </div>
        
        {/* FIXED: Removed <style jsx> and just use the CSS class */}
        <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
            {orders.length === 0 ? (
            <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📋</span>
                </div>
                <p className="text-gray-500 font-medium">No orders yet</p>
                <p className="text-gray-400 text-sm">Create your first order to get started!</p>
            </div>
            ) : (
            orders.map((order, index) => {
                const statusConfig = getStatusConfig(order.status)
                return (
                <div
                    key={order.id}
                    className={`border-2 ${statusConfig.bg} rounded-xl p-4 hover:shadow-md transition-all duration-200 transform hover:-translate-y-1`}
                    style={{ animationDelay: `${index * 100}ms` }}
                >
                    <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-gray-600 to-gray-700 rounded-lg flex items-center justify-center">
                        <span className="text-white text-xs font-bold">#{order.id}</span>
                        </div>
                        <div>
                        <div className="font-bold text-gray-800">{order.customer_name}</div>
                        <div className="text-xs text-gray-500">Order #{order.id}</div>
                        </div>
                    </div>
                    <div className={`${statusConfig.color} text-white px-3 py-1 rounded-lg flex items-center gap-1 text-xs font-semibold`}>
                        <span>{statusConfig.icon}</span>
                        {order.status}
                    </div>
                    </div>
                    
                    <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2 text-gray-600">
                        <span>{restaurantIcons[order.restaurant_type]}</span>
                        <span className="font-medium">{order.restaurant_type}</span>
                        <span className="text-gray-400">from ({order.pickup_x}, {order.pickup_y})</span>
                    </div>
                    
                    <div className="flex items-center gap-2 text-gray-600">
                        <span>🏠</span>
                        <span>To ({order.delivery_x}, {order.delivery_y})</span>
                    </div>
                    
                    <div className="flex items-center justify-between pt-2 border-t border-gray-200">
                        {order.bot_id && (
                        <div className="flex items-center gap-1 text-blue-600">
                            <span>🤖</span>
                            <span className="text-xs font-medium">Bot #{order.bot_id}</span>
                        </div>
                        )}
                        {order.estimated_time && (
                        <div className="flex items-center gap-1 text-gray-500">
                            <span>⏱️</span>
                            <span className="text-xs">ETA: {order.estimated_time}s</span>
                        </div>
                        )}
                    </div>
                    </div>
                </div>
                )
            })
            )}
        </div>
        </div>
    )
}

export default OrderList