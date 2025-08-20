// hooks/useApi.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ApiService } from '../services/api'
import type { CreateOrderRequest } from '../types'

// Query keys for consistent cache management
export const queryKeys = {
    health: ['health'] as const,
    mapGrid: ['map', 'grid'] as const,
    restaurants: ['map', 'restaurants'] as const,
    deliveryPoints: ['map', 'deliveryPoints'] as const,
    systemStats: ['map', 'stats'] as const,
    bots: ['bots'] as const,
    bot: (id: number) => ['bots', id] as const,
    botRoute: (id: number) => ['bots', id, 'route'] as const,
    botOrders: (id: number) => ['bots', id, 'orders'] as const,
    orders: ['orders'] as const,
    order: (id: number) => ['orders', id] as const,
    ordersByStatus: (status: string) => ['orders', 'status', status] as const,
} as const

// Health Check
export const useHealthCheck = () => {
    return useQuery({
        queryKey: queryKeys.health,
        queryFn: ApiService.healthCheck,
        staleTime: 30000, // 30 seconds
        refetchInterval: 60000, // 1 minute
    })
}

// Map & Grid Hooks
export const useMapGrid = () => {
    return useQuery({
        queryKey: queryKeys.mapGrid,
        queryFn: ApiService.getMapGrid,
        staleTime: 1000, // 1 second
        refetchInterval: 2000, // 2 seconds for real-time updates
    })
}

export const useRestaurants = () => {
    return useQuery({
        queryKey: queryKeys.restaurants,
        queryFn: ApiService.getRestaurants,
        staleTime: 5 * 60 * 1000, // 5 minutes (restaurants don't change often)
    })
}

export const useDeliveryPoints = () => {
    return useQuery({
        queryKey: queryKeys.deliveryPoints,
        queryFn: ApiService.getDeliveryPoints,
        staleTime: 5 * 60 * 1000, // 5 minutes
    })
}

export const useSystemStats = () => {
    return useQuery({
        queryKey: queryKeys.systemStats,
        queryFn: ApiService.getSystemStats,
        staleTime: 2000, // 2 seconds
        refetchInterval: 5000, // 5 seconds
    })
}

// Bot Hooks
export const useBots = () => {
    return useQuery({
        queryKey: queryKeys.bots,
        queryFn: ApiService.getAllBots,
        staleTime: 1000, // 1 second
        refetchInterval: 3000, // 3 seconds
    })
}

export const useBot = (botId: number) => {
    return useQuery({
        queryKey: queryKeys.bot(botId),
        queryFn: () => ApiService.getBot(botId),
        enabled: !!botId,
        staleTime: 2000,
    })
}

export const useBotRoute = (botId: number) => {
    return useQuery({
        queryKey: queryKeys.botRoute(botId),
        queryFn: () => ApiService.getBotRoute(botId),
        enabled: !!botId,
        staleTime: 5000,
    })
}

export const useBotOrders = (botId: number) => {
    return useQuery({
        queryKey: queryKeys.botOrders(botId),
        queryFn: () => ApiService.getBotOrders(botId),
        enabled: !!botId,
        staleTime: 2000,
    })
}

// Order Hooks
export const useOrders = () => {
    return useQuery({
        queryKey: queryKeys.orders,
        queryFn: ApiService.getAllOrders,
        staleTime: 1000, // 1 second
        refetchInterval: 2000, // 2 seconds for real-time updates
    })
}

export const useOrdersByStatus = (status: string) => {
    return useQuery({
        queryKey: queryKeys.ordersByStatus(status),
        queryFn: () => ApiService.getOrdersByStatus(status),
        enabled: !!status,
        staleTime: 2000,
    })
}

export const useOrder = (orderId: number) => {
    return useQuery({
        queryKey: queryKeys.order(orderId),
        queryFn: () => ApiService.getOrder(orderId),
        enabled: !!orderId,
        staleTime: 1000,
    })
}

// Mutation Hooks
export const useCreateOrder = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: (orderData: CreateOrderRequest) => ApiService.createOrder(orderData),
        onSuccess: () => {
        // Invalidate and refetch related queries
        queryClient.invalidateQueries({ queryKey: queryKeys.orders })
        queryClient.invalidateQueries({ queryKey: queryKeys.mapGrid })
        queryClient.invalidateQueries({ queryKey: queryKeys.systemStats })
        queryClient.invalidateQueries({ queryKey: queryKeys.bots })
        },
        onError: (error) => {
        console.error('Failed to create order:', error)
        },
    })
}

export const useMoveBot = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: ({ botId, x, y }: { botId: number ; x: number ; y: number }) => 
        ApiService.moveBot(botId, x, y),
        onSuccess: (data, variables) => {
        // Invalidate related queries
        queryClient.invalidateQueries({ queryKey: queryKeys.bots })
        queryClient.invalidateQueries({ queryKey: queryKeys.bot(variables.botId) })
        queryClient.invalidateQueries({ queryKey: queryKeys.mapGrid })
        queryClient.invalidateQueries({ queryKey: queryKeys.orders })
        },
        onError: (error) => {
        console.error('Failed to move bot:', error)
        },
    })
}

export const useUpdateOrderStatus = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: ({ orderId, status }: { orderId: number ; status: string }) => 
        ApiService.updateOrderStatus(orderId, status),
        onSuccess: (data, variables) => {
        // Invalidate related queries
        queryClient.invalidateQueries({ queryKey: queryKeys.orders })
        queryClient.invalidateQueries({ queryKey: queryKeys.order(variables.orderId) })
        queryClient.invalidateQueries({ queryKey: queryKeys.mapGrid })
        queryClient.invalidateQueries({ queryKey: queryKeys.systemStats })
        },
    })
}

export const useCancelOrder = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: (orderId: number) => ApiService.cancelOrder(orderId),
        onSuccess: (data, orderId) => {
        // Invalidate related queries
        queryClient.invalidateQueries({ queryKey: queryKeys.orders })
        queryClient.invalidateQueries({ queryKey: queryKeys.order(orderId) })
        queryClient.invalidateQueries({ queryKey: queryKeys.mapGrid })
        queryClient.invalidateQueries({ queryKey: queryKeys.systemStats })
        queryClient.invalidateQueries({ queryKey: queryKeys.bots })
        },
    })
}

export const useRebalanceOrders = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: ApiService.rebalanceOrders,
        onSuccess: () => {
        // Invalidate all order and bot related queries
        queryClient.invalidateQueries({ queryKey: queryKeys.orders })
        queryClient.invalidateQueries({ queryKey: queryKeys.bots })
        queryClient.invalidateQueries({ queryKey: queryKeys.mapGrid })
        queryClient.invalidateQueries({ queryKey: queryKeys.systemStats })
        },
    })
}