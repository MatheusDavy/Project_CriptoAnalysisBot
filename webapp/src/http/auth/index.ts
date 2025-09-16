import { api } from "http/api";
import type { AuthenticateProps } from "./type";

export const authenticate = async (props: AuthenticateProps) => {
  return await api.get('auth/login', { searchParams: props })
};

export const logout = async () => {
  return await api.get('auth/logout')
}