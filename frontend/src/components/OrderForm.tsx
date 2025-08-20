import React, { useState } from 'react';
import type { Restaurant, DeliveryPoint, CreateOrderRequest } from '../types';
import type { UseMutationResult } from '@tanstack/react-query';

interface OrderFormProps {
    restaurants: Restaurant[];
    deliveryPoints: DeliveryPoint[];
    onOrderCreated: () => void;
    createOrderMutation: UseMutationResult<any, Error, CreateOrderRequest, unknown>;
}

const OrderForm: React.FC<OrderFormProps> = ({ 
    restaurants, 
    deliveryPoints, 
    onOrderCreated, 
    createOrderMutation 
}) => {
    const [formData, setFormData] = useState({
        customer_name: '',
        customer_phone: '',
        restaurant_type: '' as 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI' | '',
        pickup_x: 0,
        pickup_y: 0,
        delivery_x: 0,
        delivery_y: 0
    });
    const [error, setError] = useState('');

    const handleSubmit = async () => {
        if (!formData.customer_name || !formData.restaurant_type || !formData.delivery_x) {
        setError('Please fill in all required fields');
        return;
        }

        setError('');
        
        try {
        await createOrderMutation.mutateAsync({
            customer_name: formData.customer_name,
            customer_phone: formData.customer_phone || undefined,
            restaurant_type: formData.restaurant_type,
            pickup_x: formData.pickup_x,
            pickup_y: formData.pickup_y,
            delivery_x: formData.delivery_x,
            delivery_y: formData.delivery_y
        });
        
        setFormData({
            customer_name: '',
            customer_phone: '',
            restaurant_type: '',
            pickup_x: 0,
            pickup_y: 0,
            delivery_x: 0,
            delivery_y: 0
        });
        onOrderCreated();
        } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to create order');
        }
    };

    const handleRestaurantChange = (restaurantType: string) => {
        const restaurant = restaurants.find(r => r.restaurant_type === restaurantType);
        if (restaurant) {
        setFormData(prev => ({
            ...prev,
            restaurant_type: restaurantType as 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI',
            pickup_x: restaurant.x,
            pickup_y: restaurant.y
        }));
        }
    };

    const restaurantIcons: Record<string, string> = {
        RAMEN: '🍜',
        PIZZA: '🍕', 
        CURRY: '🍛',
        SUSHI: '🍣'
    };

    return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-lg">📝</span>
            </div>
            <h2 className="text-xl font-bold text-gray-800">Create New Order</h2>
        </div>
        
        {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r-lg">
            <div className="flex items-center">
                <span className="text-red-500 mr-2">⚠️</span>
                <span className="text-red-700 font-medium">{error}</span>
            </div>
            </div>
        )}

        <div className="space-y-5">
            <div className="group">
            <label className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                👤 Customer Name
                <span className="text-red-500">*</span>
            </label>
            <input
                type="text"
                value={formData.customer_name}
                onChange={(e) => setFormData(prev => ({...prev, customer_name: e.target.value}))}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all group-hover:border-gray-300"
                placeholder="Enter customer name"
                required
            />
            </div>

            <div className="group">
            <label className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                📞 Phone Number
            </label>
            <input
                type="text"
                value={formData.customer_phone}
                onChange={(e) => setFormData(prev => ({...prev, customer_phone: e.target.value}))}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all group-hover:border-gray-300"
                placeholder="Optional phone number"
            />
            </div>

            <div className="group">
            <label className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                🏪 Restaurant
                <span className="text-red-500">*</span>
            </label>
            <select
                value={formData.restaurant_type}
                onChange={(e) => handleRestaurantChange(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all group-hover:border-gray-300"
                required
            >
                <option value="">Select Restaurant</option>
                {restaurants.map(restaurant => (
                <option key={restaurant.id} value={restaurant.restaurant_type}>
                    {restaurantIcons[restaurant.restaurant_type]} {restaurant.name} ({restaurant.restaurant_type}) - ({restaurant.x}, {restaurant.y})
                </option>
                ))}
            </select>
            </div>

            <div className="group">
            <label className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                🏠 Delivery Address
                <span className="text-red-500">*</span>
            </label>
            <select
                value={`${formData.delivery_x},${formData.delivery_y}`}
                onChange={(e) => {
                const [xStr, yStr] = e.target.value.split(',');
                const x = Number(xStr);
                const y = Number(yStr);
                setFormData(prev => ({...prev, delivery_x: x, delivery_y: y}));
                }}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all group-hover:border-gray-300"
                required
            >
                <option value="0,0">Select Delivery Address</option>
                {deliveryPoints.map(point => (
                <option key={point.id} value={`${point.x},${point.y}`}>
                    🏠 {point.name} - ({point.x}, {point.y})
                </option>
                ))}
            </select>
            </div>

            <button
            onClick={handleSubmit}
            disabled={createOrderMutation?.isPending}
            className={`w-full py-4 px-6 rounded-lg text-white font-semibold text-lg transition-all transform ${
                createOrderMutation?.isPending
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            }`}
            >
            <div className="flex items-center justify-center gap-2">
                {createOrderMutation?.isPending ? (
                <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Creating Order...
                </>
                ) : (
                <>
                    <span>🚀</span>
                    Create Order
                </>
                )}
            </div>
            </button>
        </div>
        </div>
    );
};

export default OrderForm;