// services/NavigationService.js
let navigateFunction;

export const setNavigate = (nav) => {
  navigateFunction = nav;
};

export const redirectToLogin = () => {
  if (navigateFunction) {
    navigateFunction('/login');
  } else {
    // Fallback to full page reload if navigate isn't set
    window.location.href = '/login';
  }
};

