import React from 'react';
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
} from 'react-icons/fa';
import { 
  MdDeliveryDining,
  MdRestaurant,
  MdRamenDining
} from 'react-icons/md';
import { GiBowlOfRice, GiSushis } from 'react-icons/gi';

// Food type icons
export const FOOD_ICONS = {
  RAMEN: <MdRamenDining className="text-current" />,
  PIZZA: <FaPizzaSlice className="text-current" />,
  CURRY: <GiBowlOfRice className="text-current" />,
  SUSHI: <GiSushis className="text-current" />
};

// UI Component Icons
export const UI_ICONS = {
  // Form icons
  USER: <FaUser className="text-current" />,
  PHONE: <FaPhone className="text-current" />,
  HOME: <FaHome className="text-current" />,
  RESTAURANT: <FaStore className="text-current" />,
  ROCKET: <FaRocket className="text-current" />,
  CLIPBOARD: <FaClipboardList className="text-current" />,
  
  // Map icons
  DELIVERY_POINT: <FaHome className="text-current" />,
  BOT_STATION: <FaBolt className="text-current" />,
  BLOCKED: <FaBan className="text-current" />,
  TARGET: <FaCrosshairs className="text-current" />,
  
  // Status and action icons
  WARNING: <FaExclamationTriangle className="text-current" />,
  REFRESH: <FaRedoAlt className="text-current" />,
  TIMER: <FaClock className="text-current" />
};

// Order status icons
export const ORDER_STATUS_ICONS = {
  PENDING: <FaClock className="text-current" />,
  ASSIGNED: <FaSpinner className="text-current" />,
  PICKED_UP: <FaBox className="text-current" />,
  DELIVERED: <FaCheckCircle className="text-current" />,
  CANCELLED: <FaTimesCircle className="text-current" />,
  default: <FaQuestionCircle className="text-current" />
};

// System stats icons
export const SYSTEM_STATS_ICONS = {
  PENDING: <FaClock className="text-current" />,
  ACTIVE: <FaRocket className="text-current" />,
  DELIVERED: <FaCheckCircle className="text-current" />
};

// Helper function to get food icon by type
export const getFoodIcon = (foodType: string) => {
  return FOOD_ICONS[foodType as keyof typeof FOOD_ICONS] || <MdRestaurant className="text-current" />;
};

// Helper function to get order status icon
export const getOrderStatusIcon = (status: string) => {
  return ORDER_STATUS_ICONS[status as keyof typeof ORDER_STATUS_ICONS] || ORDER_STATUS_ICONS.default;
};
