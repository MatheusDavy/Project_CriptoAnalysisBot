import { api } from "http/api";
import type { GainTargetTypes, LossTargetTypes } from "types/settings";

//------------------------------------//
export type CreateSettingsProps = {
  name: string;
  indicators: string[];
  candle_patterns: string[];
  timeranges: string[];
  timeframes: string[];
  currencies: string[];
  min_confluence: number;
  gain_target: {
    type: GainTargetTypes;
    value: number;
  }[];
  loss_target: {
    type: LossTargetTypes;
    value: number;
  }[];
};

export const creteSettings = (body: CreateSettingsProps) => {
  return api.post("settings/create", {
    json: body,
  });
};

//------------------------------------//
export type UpdateSettingsProps = {
  id: string;
  status?: boolean
  name?: string;
  indicators?: string[];
  candle_patterns?: string[];
  timeranges?: string[];
  timeframes?: string[];
  currencies?: string[];
  min_confluence?: number;
  gain_target?: {
    type: GainTargetTypes;
    value: number;
  }[];
  loss_target?: {
    type: LossTargetTypes;
    value: number;
  }[];
};

export const updateSettings = ({ id, ...body}: UpdateSettingsProps) => {
  return api.put(`settings/update/${id}`, {
    json: body,
  });
};

//------------------------------------//
export const deleteSettings = async (id: string) => {
 return api.delete(`settings/delete/${id}`);
};

//------------------------------------//
export type ListSettingsTypes = {
  id: string;
  status: boolean
  name: string;
  indicators: string[];
  candle_patterns: string[];
  timeranges: string[];
  timeframes: string[];
  currencies: string[];
  min_confluence: number;
  gain_target: {
    type: GainTargetTypes;
    value: number;
  }[];
  loss_target: {
    type: LossTargetTypes;
    value: number;
  }[];
}[];

export const listSettings = async () => {
  const result = await api.get<ListSettingsTypes>("settings/list");
  
  if (!result.ok) return []

  return result.json()
};

//------------------------------------//
export type GetSettingsTypes = ListSettingsTypes[number]

export const getSettings = async (id: string) => {
  const result = await api.get<GetSettingsTypes>(`settings/${id}`);
  
  if (!result.ok) return;

  return result.json()
};
