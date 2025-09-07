import { useState, useEffect } from 'react';

const breakpoints = {
  mobile: 0,
  tablet: 768,
  desktop: 1250,
};

export function useViewport() {
  const getViewport = () => {
    if (typeof window === 'undefined') return 'desktop'; // Fallback for SSR or undefined window
    const width = window.innerWidth;
    if (width < breakpoints.tablet) {
      return 'mobile';
    } 
    else if (width < breakpoints.desktop) {
      return 'tablet';
    }
    else if (width > breakpoints.desktop){
      return 'desktop';
    }
  };

  const [viewport, setViewport] = useState(getViewport()); // Call the function immediately to set the initial value

  useEffect(() => {
    const determineViewport = () => {
      setViewport(getViewport()); // Update viewport dynamically
    };

    window.addEventListener('resize', determineViewport);

    // Cleanup event listener on unmount
    return () => {
      window.removeEventListener('resize', determineViewport);
    };
  }, []);

  return viewport;
}
