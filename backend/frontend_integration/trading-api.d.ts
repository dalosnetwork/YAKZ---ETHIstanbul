/**
 * TypeScript definitions for Trading API
 */

export interface AccountInfo {
  accountType: string;
  canTrade: boolean;
  canWithdraw: boolean;
  canDeposit: boolean;
  balances: Balance[];
}

export interface Balance {
  asset: string;
  free: string;
  locked: string;
}

export interface SymbolInfo {
  symbol: string;
  status: string;
  baseAsset: string;
  quoteAsset: string;
  filters: {
    minQty: string;
    maxQty: string;
    stepSize: string;
    minPrice: string;
    maxPrice: string;
    tickSize: string;
  };
}

export interface Order {
  orderId: number;
  symbol: string;
  side: 'BUY' | 'SELL';
  type: 'MARKET' | 'LIMIT';
  quantity: string;
  price: string;
  status: 'NEW' | 'FILLED' | 'CANCELED' | 'REJECTED';
  time: number;
}

export interface DEXQuote {
  pathId: string;
  inValues: string[];
  outValues: string[];
  gasEstimate: number;
  priceImpact: number;
  slippageLimitPercent: number;
}

export interface DEXTransaction {
  to: string;
  value: string;
  data: string;
  gas: number;
  gasPrice: number;
}

export interface DEXAssembleResult {
  transaction: DEXTransaction;
  simulation: {
    isSuccess: boolean;
    amountsOut: string[];
  };
}

export interface SystemStatus {
  trading_enabled: boolean;
  testnet_mode: boolean;
  supported_chains: number[];
  supported_tokens: Record<string, string[]>;
}

export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  timestamp: number;
  services: {
    binance: 'connected' | 'disconnected';
    odos: 'available' | 'unavailable';
    contract_listener: 'running' | 'stopped';
  };
}

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: string;
  };
}

export interface TradingEvent {
  exchange: string;
  quantity: number;
  price: number;
  pair: string;
  side: 'buy' | 'sell';
}

export interface WebSocketMessage {
  type: string;
  data: any;
}

export class TradingAPI {
  constructor(apiKey: string, baseURL?: string);
  
  // Account methods
  getAccountInfo(): Promise<APIResponse<AccountInfo>>;
  getBalance(asset: string): Promise<APIResponse<{ asset: string; balance: number }>>;
  
  // Market data methods
  getSymbolInfo(symbol: string): Promise<APIResponse<SymbolInfo>>;
  getOpenOrders(): Promise<APIResponse<Order[]>>;
  
  // Trading methods
  placeBuyOrder(symbol: string, quantity: number): Promise<APIResponse<Order>>;
  placeSellOrder(symbol: string, quantity: number): Promise<APIResponse<Order>>;
  cancelOrder(orderId: number, symbol?: string): Promise<APIResponse<Order>>;
  
  // DEX methods
  getDEXQuote(tokenIn: string, tokenOut: string, amount: string, chainId: number): Promise<APIResponse<DEXQuote>>;
  assembleDEXTransaction(pathId: string, userAddress: string): Promise<APIResponse<DEXAssembleResult>>;
  
  // Event methods
  triggerEvent(eventData: string): Promise<APIResponse<{ message: string; event_data: string }>>;
  
  // System methods
  healthCheck(): Promise<APIResponse<HealthStatus>>;
  getSystemStatus(): Promise<APIResponse<SystemStatus>>;
  
  // WebSocket methods
  connectWebSocket(): WebSocket;
  disconnectWebSocket(): void;
  on(event: string, callback: (data: any) => void): void;
  off(event: string, callback: (data: any) => void): void;
  emit(event: string, data: any): void;
  
  // Utility methods
  formatTradingEvent(exchange: string, quantity: number, price: number, pair: string, side: string): string;
  parseTradingEvent(eventData: string): TradingEvent;
  getSupportedChains(): Record<number, string>;
  getTokenAddresses(chainId: number): Record<string, string>;
}

// React Hook types
export interface UseAccountInfoReturn {
  accountInfo: AccountInfo | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseBalanceReturn {
  balance: number | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseOpenOrdersReturn {
  orders: Order[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseTradingReturn {
  placeBuyOrder: (symbol: string, quantity: number) => Promise<Order>;
  placeSellOrder: (symbol: string, quantity: number) => Promise<Order>;
  cancelOrder: (orderId: number, symbol?: string) => Promise<Order>;
  loading: boolean;
  error: string | null;
}

export interface UseDEXReturn {
  getQuote: (tokenIn: string, tokenOut: string, amount: string, chainId: number) => Promise<DEXQuote>;
  assembleTransaction: (pathId: string, userAddress: string) => Promise<DEXAssembleResult>;
  loading: boolean;
  error: string | null;
}

export interface UseWebSocketReturn {
  connected: boolean;
  messages: WebSocketMessage[];
  error: string | null;
  connect: () => void;
  disconnect: () => void;
}

export interface UseSystemStatusReturn {
  status: SystemStatus | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseEventsReturn {
  triggerEvent: (eventData: string) => Promise<{ message: string; event_data: string }>;
  triggerTradingEvent: (exchange: string, quantity: number, price: number, pair: string, side: string) => Promise<{ message: string; event_data: string }>;
  loading: boolean;
  error: string | null;
}

// Hook function types
export declare function useAccountInfo(apiKey: string, autoFetch?: boolean): UseAccountInfoReturn;
export declare function useBalance(apiKey: string, asset: string, autoFetch?: boolean): UseBalanceReturn;
export declare function useOpenOrders(apiKey: string, autoFetch?: boolean): UseOpenOrdersReturn;
export declare function useTrading(apiKey: string): UseTradingReturn;
export declare function useDEX(apiKey: string): UseDEXReturn;
export declare function useWebSocket(apiKey: string): UseWebSocketReturn;
export declare function useSystemStatus(apiKey: string, autoFetch?: boolean): UseSystemStatusReturn;
export declare function useEvents(apiKey: string): UseEventsReturn;
