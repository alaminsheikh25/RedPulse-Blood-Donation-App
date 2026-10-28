import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  },
);

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
}

export interface Donor {
  id: string;
  user_id: string;
  blood_group: string;
  date_of_birth: string;
  gender: string;
  weight_kg: number;
  latitude?: number;
  longitude?: number;
  city?: string;
  state?: string;
  hemoglobin_g_dl?: number;
  last_donation_date?: string;
  total_donations: number;
  is_available: boolean;
  is_eligible: boolean;
  deferred_until?: string;
  reliability_score: number;
  response_rate: number;
}

export interface BloodRequest {
  id: string;
  requester_user_id: string;
  hospital_id?: string;
  patient_name?: string;
  patient_age?: number;
  blood_group: string;
  units_required: number;
  units_fulfilled: number;
  urgency: string;
  status: string;
  needed_by?: string;
  latitude?: number;
  longitude?: number;
  location_description?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Hospital {
  id: string;
  name: string;
  address: string;
  city: string;
  state?: string;
  phone?: string;
  email?: string;
  has_blood_bank: boolean;
  is_verified: boolean;
  is_active: boolean;
}

export interface InventoryItem {
  id: string;
  hospital_id: string;
  blood_group: string;
  units_available: number;
  units_reserved: number;
  status: string;
  expiry_date?: string;
  batch_number?: string;
  storage_location?: string;
}

export interface Donation {
  id: string;
  donor_id: string;
  hospital_id?: string;
  request_id?: string;
  donation_type: string;
  status: string;
  scheduled_date?: string;
  donation_date?: string;
  units: number;
}

export interface Appointment {
  id: string;
  donor_id: string;
  hospital_id: string;
  scheduled_at: string;
  duration_minutes: number;
  status: string;
  notes?: string;
}

export interface Campaign {
  id: string;
  title: string;
  status: string;
  start_date: string;
  end_date: string;
}

export interface Summary {
  total_donors: number;
  total_requests: number;
  total_donations: number;
  units_available: number;
}
