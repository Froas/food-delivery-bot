export interface Bot {
    id: number
    name: string
    current_x: number
    current_y: number
    max_capacity: number
    status: 'IDLE' | 'BUSY' | 'MAINTENANCE'
    current_orders: number
    battery_level: number
    created_at: string
    updated_at: string
}

export interface Order {
    id: number
    customer_name: string
    customer_phone: string | null
    restaurant_type: 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI'
    pickup_x: number
    pickup_y: number
    delivery_x: number
    delivery_y: number
    status: 'PENDING' | 'ASSIGNED' | 'PICKED_UP' | 'DELIVERED' | 'CANCELLED'
    bot_id: number | null
    priority: number
    estimated_distance: number | null
    estimated_time: number | null
    created_at: string
    updated_at: string
}

export interface CreateOrderRequest {
    customer_name: string
    customer_phone?: string
    restaurant_type: 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI'
    pickup_x: number
    pickup_y: number
    delivery_x: number
    delivery_y: number
}

export interface Restaurant {
    id: number
    x: number
    y: number
    restaurant_type: 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI'
    name: string
}

export interface DeliveryPoint {
    id: number
    x: number
    y: number
    name: string
}

export interface BlockedPath {
    from: {
        x: number
        y: number
        id: number
    }
    to: {
        x: number
        y: number
        id: number
    }
    created_at: string
}

export interface BlockedSegment {
    from_x: number
    from_y: number
    to_x: number
    to_y: number
    direction: 'right' | 'left' | 'down' | 'up' | 'diagonal'
}

export interface BlockedPathsResponse {
    blocked_paths: BlockedPath[]
    total_blocked: number
    visualization_data: {
        blocked_segments: BlockedSegment[]
    }
}

export interface GridCell {
    x: number
    y: number
    node_type: 'NODE' | 'HOUSE' | 'RESTAURANT' | 'BOT_STATION'
    is_delivery_point: boolean
    is_restaurant: boolean
    is_bot_station: boolean
    restaurant_type: string | null
    name: string
    bots: Array<{
        id: number
        name: string
        status: string
        current_orders: number
        battery_level: number
    }>
    active_orders: Array<{
        id: number
        customer_name: string
        restaurant_type: string
        status: string
        bot_id: number | null
        location_type: 'pickup' | 'delivery'
    }>
    // NEW: Blocked path information
    blocked_paths?: {
        right?: boolean
        left?: boolean
        down?: boolean
        up?: boolean
    }
}

export interface MapGrid {
    grid: Record<string, GridCell>
    grid_size: number
    total_nodes: number
    total_bots: number
    active_orders: number
}

export interface SystemStats {
    map: {
        total_nodes: number
        restaurants: number
        houses: number
        bot_stations: number
    }
    bots: {
        total: number
        idle: number
        busy: number
    }
    orders: {
        pending: number
        active: number
        delivered: number
    }
}

export interface BotRoute {
    route_points: Array<{
        x: number
        y: number
        type: 'start' | 'pickup' | 'delivery'
        order_id: number | null
        restaurant_type?: string
        customer_name?: string
    }>
    total_distance: number
    estimated_time: number
    detailed_path: Array<{ x: number ; y: number }>
}

export interface ApiError {
    detail: string
}