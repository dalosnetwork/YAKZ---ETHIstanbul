// src/hooks/useNumberFormatter.js
import { useMemo } from 'react';
import { formatNumber } from '../utils/numberFormatter';

export const useNumberFormatter = (input) => {
  const formattedNumber = useMemo(() => formatNumber(input), [input]);
  return formattedNumber;
};
