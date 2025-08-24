import React from 'react'
import { 
  FaPizzaSlice,
  FaHome,
  FaStore,
  FaUser,
  FaPhone,
  FaRocket,
  FaClipboardList,
  FaClock,
  FaSpinner,
  FaBox,
  FaCheckCircle,
  FaTimesCircle,
  FaQuestionCircle,
  FaExclamationTriangle,
  FaRedoAlt,
  FaBolt,
  FaBan,
  FaCrosshairs
} from 'react-icons/fa'
import { 
  MdDeliveryDining,
  MdRestaurant,
  MdRamenDining
} from 'react-icons/md'
import { GiBowlOfRice, GiSushis } from 'react-icons/gi'


export const FOOD_ICONS = {
  RAMEN: <MdRamenDining className="text-current" />,
  PIZZA: <FaPizzaSlice className="text-current" />,
  CURRY: <GiBowlOfRice className="text-current" />,
  SUSHI: <GiSushis className="text-current" />
}


export const UI_ICONS = {

  USER: <FaUser className="text-current" />,
  PHONE: <FaPhone className="text-current" />,
  HOME: <FaHome className="text-current" />,
  RESTAURANT: <FaStore className="text-current" />,
  ROCKET: <FaRocket className="text-current" />,
  CLIPBOARD: <FaClipboardList className="text-current" />,

  DELIVERY_POINT: <FaHome className="text-current" />,
  BOT_STATION: <FaBolt className="text-current" />,
  BLOCKED: <FaBan className="text-current" />,
  TARGET: <FaCrosshairs className="text-current" />,
  
  WARNING: <FaExclamationTriangle className="text-current" />,
  REFRESH: <FaRedoAlt className="text-current" />,
  TIMER: <FaClock className="text-current" />
}

export const ORDER_STATUS_ICONS = {
  PENDING: <FaClock className="text-current" />,
  ASSIGNED: <FaSpinner className="text-current" />,
  PICKED_UP: <FaBox className="text-current" />,
  DELIVERED: <FaCheckCircle className="text-current" />,
  CANCELLED: <FaTimesCircle className="text-current" />,
  default: <FaQuestionCircle className="text-current" />
}

export const SYSTEM_STATS_ICONS = {
  PENDING: <FaClock className="text-current" />,
  ACTIVE: <FaRocket className="text-current" />,
  DELIVERED: <FaCheckCircle className="text-current" />
}

export const getFoodIcon = (foodType: string) => {
  return FOOD_ICONS[foodType as keyof typeof FOOD_ICONS] || <MdRestaurant className="text-current" />
}

export const getOrderStatusIcon = (status: string) => {
  return ORDER_STATUS_ICONS[status as keyof typeof ORDER_STATUS_ICONS] || ORDER_STATUS_ICONS.default
}
