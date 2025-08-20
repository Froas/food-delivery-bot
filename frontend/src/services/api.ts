import axios from 'axios'
import type { AxiosResponse } from 'axios'

import type {
    Bot,
    Order,
    CreateOrderRequest,
    Restaurant,
    DeliveryPoint,
    MapGrid,
    SystemStats,
    BotRoute,
    ApiError
} from '../types'

const API_BASE_URL = 'http://localhost:8000'

// Create axios instance with base configuration
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor for logging
apiClient.interceptors.request.use(
    (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
    },
    (error) => {
        console.error('❌ API Request Error:', error)
        return Promise.reject(error)
    }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`)
        return response
    },
    (error) => {
        console.error('❌ API Response Error:', error.response?.data || error.message)
        return Promise.reject(error)
    }
)

export class ApiService {
  // Health check
    static async healthCheck(): Promise<{ status: string ; version: string }> {
        const response: AxiosResponse = await apiClient.get('/health')
        return response.data
    }

  // Map & Grid APIs
    static async getMapGrid(): Promise<MapGrid> {
        const response: AxiosResponse<MapGrid> = await apiClient.get('/api/v1/map/grid')
        return response.data
    }

    static async getRestaurants(): Promise<Restaurant[]> {
        const response: AxiosResponse<Restaurant[]> = await apiClient.get('/api/v1/map/restaurants')
        return response.data
    }

    static async getDeliveryPoints(): Promise<DeliveryPoint[]> {
        const response: AxiosResponse<DeliveryPoint[]> = await apiClient.get('/api/v1/map/delivery-points')
        return response.data
    }

    static async getSystemStats(): Promise<SystemStats> {
        const response: AxiosResponse<SystemStats> = await apiClient.get('/api/v1/map/stats')
        return response.data
    }

    // Bot APIs
    static async getAllBots(): Promise<Bot[]> {
        const response: AxiosResponse<Bot[]> = await apiClient.get('/api/v1/bots/')
        return response.data
    }

    static async getBot(botId: number): Promise<Bot> {
        const response: AxiosResponse<Bot> = await apiClient.get(`/api/v1/bots/${botId}`)
        return response.data
    }

    static async moveBot(botId: number, x: number, y: number): Promise<{ message: string ; new_position: { x: number ; y: number } ; bot_id: number }> {
        const response: AxiosResponse = await apiClient.post(`/api/v1/bots/${botId}/move?x=${x}&y=${y}`)
        return response.data
    }

    static async getBotRoute(botId: number): Promise<BotRoute> {
        const response: AxiosResponse<BotRoute> = await apiClient.get(`/api/v1/bots/${botId}/route`)
        return response.data
    }

    static async getBotOrders(botId: number): Promise<Order[]> {
        const response: AxiosResponse<Order[]> = await apiClient.get(`/api/v1/bots/${botId}/orders`)
        return response.data
    }

    // Order APIs
    static async getAllOrders(): Promise<Order[]> {
        const response: AxiosResponse<Order[]> = await apiClient.get('/api/v1/orders/')
        return response.data
    }

    static async getOrdersByStatus(status: string): Promise<Order[]> {
        const response: AxiosResponse<Order[]> = await apiClient.get(`/api/v1/orders/?status=${status}`)
        return response.data
    }

    static async getOrder(orderId: number): Promise<Order> {
        const response: AxiosResponse<Order> = await apiClient.get(`/api/v1/orders/${orderId}`)
        return response.data
    }

    static async createOrder(orderData: CreateOrderRequest): Promise<Order> {
        const response: AxiosResponse<Order> = await apiClient.post('/api/v1/orders/', orderData)
        return response.data
    }

    static async updateOrderStatus(orderId: number, status: string): Promise<Order> {
        const response: AxiosResponse<Order> = await apiClient.put(`/api/v1/orders/${orderId}`, { status })
        return response.data
    }

    static async cancelOrder(orderId: number): Promise<{ message: string }> {
        const response: AxiosResponse = await apiClient.delete(`/api/v1/orders/${orderId}`)
        return response.data
    }

    // Route APIs
    static async calculateDistance(startX: number, startY: number, endX: number, endY: number) {
        const response: AxiosResponse = await apiClient.get(
        `/api/v1/routes/distance?start_x=${startX}&start_y=${startY}&end_x=${endX}&end_y=${endY}`
        )
        return response.data
    }

    static async optimizeAllRoutes() {
        const response: AxiosResponse = await apiClient.get('/api/v1/routes/optimize')
        return response.data
    }

    static async rebalanceOrders() {
        const response: AxiosResponse = await apiClient.post('/api/v1/routes/rebalance')
        return response.data
    }

    static async getEfficiencyReport() {
        const response: AxiosResponse = await apiClient.get('/api/v1/routes/efficiency')
        return response.data
    }
}

export default ApiService