import ReactGA from "react-ga4";

export const initGA = () => {
  // Replace with your actual Measurement ID
  ReactGA.initialize("G-XXXXXXXXXX"); 
};

export const logPageView = () => {
  ReactGA.send({ hitType: "pageview", page: window.location.pathname });
};

