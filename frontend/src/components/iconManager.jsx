import PropTypes from "prop-types";

export default function Icon({ name, ...props }) {
  switch (name) {
    case "gas":
      return (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
        >
          <path
            d="M20.6816 6.9751L19.8541 6.14728C19.8538 6.14703 19.8543 6.14752 19.8541 6.14728L16.8789 3.17139C16.6836 2.97607 16.3672 2.97607 16.1719 3.17139C15.9766 3.3667 15.9766 3.68311 16.1719 3.87842L17.9191 5.62592L16.9844 8.11816C16.6406 9.0332 16.8652 10.0718 17.5566 10.7642L21 14.207V19C21 20.1025 20.1025 21 19 21C17.8975 21 17 20.1025 17 19V16.5C17 15.1211 15.8789 14 14.5 14H14V4.5C14 3.12158 12.8789 2 11.5 2H4.5C3.12158 2 2 3.12158 2 4.5V19.5C2 20.8789 3.12158 22 4.5 22H11.5C12.8789 22 14 20.8789 14 19.5V15H14.5C15.3271 15 16 15.6729 16 16.5V19C16 20.6543 17.3457 22 19 22C20.6543 22 22 20.6543 22 19V10.1567C22 8.97266 21.5195 7.81299 20.6816 6.9751ZM13 19.5C13 20.3271 12.3271 21 11.5 21H4.5C3.67285 21 3 20.3271 3 19.5V11H13V19.5ZM13 10H3V4.5C3 3.67285 3.67285 3 4.5 3H11.5C12.3271 3 13 3.67285 13 4.5V10ZM21 12.793L18.2637 10.0576C17.8496 9.64209 17.7148 9.01855 17.9199 8.46973L18.6953 6.40283L19.9746 7.68213C20.626 8.33398 21 9.23584 21 10.1567V12.793Z"
            fill="#FCFCFC"
          />
        </svg>
      );
    case "swap":
      return (
        <svg
          className={props.className}
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
        >
          <path
            d="M8.72705 4V20L2.72705 14.5"
            stroke="white"
            stroke-width="3"
            stroke-linecap="square"
            stroke-linejoin="round"
          />
          <path
            d="M14.7271 20L14.7271 4L20.7271 9.5"
            stroke="white"
            stroke-width="3"
            stroke-linecap="square"
            stroke-linejoin="round"
          />
        </svg>
      );
    case "search":
      return (
        <svg
          className={props.className}
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
        >
          <path
            d="M7.33333 2.66667L4 6V11.3333L7.33333 14.6667H5.33333L2.66667 12V5.33333L5.33333 2.66667H7.33333Z"
            fill="#2040ED"
          />
          <path
            d="M16.6667 13.724L15.6667 14.724L14.276 13.3333L15.3333 12.276V5.05733L12.276 2H5.05733L2 5.05733V12.276L5.05733 15.3333H12.276L13.3333 14.276L14.724 15.6667L13.724 16.6667L19.0573 22H20.276L22 20.276V19.0573L16.6667 13.724ZM11.724 14H5.60933L3.33333 11.724V5.60933L5.60933 3.33333H11.724L14 5.60933V11.724L11.724 14ZM20.6667 19.724L19.724 20.6667H19.6093L15.6093 16.6667L16.6667 15.6093L20.6667 19.6093V19.724Z"
            fill="white"
          />
        </svg>
      );
    case "route":
      return (
        <svg
        className={props.className}
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
        >
          <path
            d="M3 17L7 21M7 17L3 21M17 3L21 7M21 3L17 7M14 5C13.4696 5 12.9609 5.21071 12.5858 5.58579C12.2107 5.96086 12 6.46957 12 7V17C12 17.5304 11.7893 18.0391 11.4142 18.4142C11.0391 18.7893 10.5304 19 10 19"
            stroke="#FCFCFC"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      );
    case "routeDropdown":
      return (
        <svg
        className={props.className}
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
        >
          <g clip-path="url(#clip0_157_3207)">
            <path
              d="M4 11L12 14L20 11"
              stroke="white"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </g>
          <defs>
            <clipPath id="clip0_157_3207">
              <rect width="24" height="24" fill="white" />
            </clipPath>
          </defs>
        </svg>
      );

    default:
      return null;
  }
}

Icon.propTypes = {
  className: PropTypes.string,
  style: PropTypes.object,
};
