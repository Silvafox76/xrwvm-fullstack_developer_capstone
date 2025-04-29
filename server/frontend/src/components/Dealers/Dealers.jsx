import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  // ✅ Update this URL if Django is deployed elsewhere
  const BASE_URL = "https://ryanwdear-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai";

  const getDealers = async () => {
    try {
      const res = await fetch(`${BASE_URL}/djangoapp/get_dealers`, { method: "GET" });
      const data = await res.json();

      if (data.status === 200) {
        const dealers = Array.from(data.dealers);
        setDealersList(dealers);
        const statesSet = new Set(dealers.map(d => d.state));
        setStates(Array.from(statesSet));
      }
    } catch (err) {
      console.error("Failed to fetch dealers:", err);
    }
  };

  const filterDealers = async (state) => {
    try {
      const endpoint = state === "All"
        ? `${BASE_URL}/djangoapp/get_dealers`
        : `${BASE_URL}/djangoapp/get_dealers/${state}`;

      const res = await fetch(endpoint, { method: "GET" });
      const data = await res.json();

      if (data.status === 200) {
        setDealersList(Array.from(data.dealers));
      }
    } catch (err) {
      console.error("Failed to fetch filtered dealers:", err);
    }
  };

  useEffect(() => {
    getDealers();
  }, []);

  const isLoggedIn = sessionStorage.getItem("username") !== null;

  return (
    <div>
      <Header />
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)} defaultValue="">
                <option value="" disabled hidden>Select State</option>
                <option value="All">All States</option>
                {states.map((state) => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.map((dealer) => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td><a href={`/dealer/${dealer.id}`}>{dealer.name}</a></td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
              <td>{dealer.state}</td>
              {isLoggedIn && (
                <td>
                  <a href={`/postreview/${dealer.id}`}>
                    <img src={review_icon} className="review_icon" alt="Post Review" />
                  </a>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dealers;
