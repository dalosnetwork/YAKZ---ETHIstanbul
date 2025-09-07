// @ts-check
import { useState } from "react";
import logo from "./design/assets/logo_long.png";
import Button1 from "./components/button1";
import React from "react";
import Icon from "./components/iconManager";
import dalos from "./design/assets/dalos_logotype_yatay_açıkrenkli 1.svg";
import { aggregate } from "./services/api";
import { useViewport } from "./hooks/useViewport";
import roar from "./design/sounds/roar.wav";
import { ethers, formatEther, getAddress, formatUnits } from "ethers";
import { truncateAddress, truncateString } from "./utils/truncateString";

function App() {
  const tokens = [
    {
      name: "ETH",
      address: "0x4200000000000000000000000000000000000006",
      img: "https://cdn.worldvectorlogo.com/logos/ethereum-eth.svg",
    },
    {
      name: "USDC",
      address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ43MuDqq54iD1ZCRL_uthAPkfwSSL-J5qI_Q&s",
    },
    {
      name: "USDT",
      address: "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
      img: "https://images.seeklogo.com/logo-png/32/1/tether-usdt-logo-png_seeklogo-323175.png",
    },
    {
      name: "LINK",
      address: "0x1D9328F2713E8b4EFca304093D53fcC2c068B7Cd",
      img: "https://s2.coinmarketcap.com/static/img/coins/200x200/1975.png",
    },
  ];

  const [fromToken, setFromToken] = useState(tokens[0]);
  const [toToken, setToToken] = useState(tokens[2]);
  const [amount, setAmount] = useState("");
  const [isRoute, setIsRoute] = useState(false);
  const [data1, setData] = useState({});
  const [signer, setSigner] = useState();
  const [address, setAddress] = useState();
  const [provider, setProvider] = useState();

  const handleSwap = () => {
    let token1 = fromToken;
    setFromToken(toToken);
    setToToken(token1);
  };

  const [searchTerm, setSearchTerm] = useState("");
  const filteredTokens = tokens.filter((token) =>
    token.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const viewport = useViewport();

  const handleFinishSwap = async () => {
    try {
      setIsRoute(true);
      const data = await aggregate(fromToken.address, "1", toToken.address);
      if (data) {
        setData(data);
        console.log("DATA1", data1);
        const audio = new Audio(roar);
        audio.preload = "auto";
        audio.play().catch((err) => console.warn("play failed", err));
      } else {
        console.log("Failed to update transaction status");
      }
    } catch (error) {
      console.error("Error updating transaction status:", error);
    }
  };

  const handleConnectWallet = async () => {
    if (!window.ethereum) {
      alert("MetaMask not found!");
      return;
    }

    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const address = await signer.getAddress();
      setSigner(signer);
      setAddress(address);
      setProvider(provider);
      getTokenBalance(fromToken.address, "from");
      getTokenBalance(toToken.address, "to");
      console.log("Wallet connected:", signer, provider, address);
    } catch (error) {
      console.error("Error connecting wallet:", error);
    }
  };

  const getTokenBalance = async (tokenAddress, fromOrTo) => {
    if (!window.ethereum) {
      console.error("MetaMask not detected");
      return;
    }

    const provider = new ethers.BrowserProvider(window.ethereum);
    const accounts = await provider.send("eth_requestAccounts", []);
    const userAddress = accounts[0];

    if (!userAddress) {
      console.error("No address found");
      return;
    }

    let balance, symbol;

    if (tokenAddress === "0x4200000000000000000000000000000000000006") {
      const rawBalance = await provider.getBalance(userAddress);
      balance = formatEther(rawBalance);
      symbol = "ETH";
    } else {
      try {
        const contractAddress = ethers.getAddress(tokenAddress);
        const erc20ABI = [
          "function balanceOf(address) view returns (uint256)",
          "function decimals() view returns (uint8)",
          "function symbol() view returns (string)",
        ];
        const tokenContract = new ethers.Contract(
          contractAddress,
          erc20ABI,
          provider
        );

        const [rawBalance, decimals, fetchedSymbol] = await Promise.all([
          tokenContract.balanceOf(userAddress),
          tokenContract.decimals(),
          tokenContract.symbol(),
        ]);

        balance = formatUnits(rawBalance, decimals);
        symbol = fetchedSymbol;
      } catch (error) {
        console.error("Error getting token balance:", error);
        return;
      }
    }

    // Update the correct token state
    const updatedToken = {
      ...(fromOrTo === "from" ? fromToken : toToken),
      balance,
    };

    if (fromOrTo === "from") {
      setFromToken(updatedToken);
    } else {
      setToToken(updatedToken);
    }

    console.log(`${symbol} Balance:`, balance);
  };

  return (
    <>
      {/* <button onClick={() => getTokenBalance("ETH")}>DENEMEBUTTON</button>
      <button
        onClick={() =>
          getTokenBalance("0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2")
        }
      >
        USDC
      </button> */}
      <section id="main">
        <video
          id="bg-video"
          autoPlay
          muted
          style={{ zIndex: "-1" }}
          loop
          playsInline
          src="/bg.mp4"
        ></video>
        <div
          className="d-flex justify-content-between"
          style={{
            overflow: "scroll",
            flexDirection: "column",
            height: "100vh",
          }}
        >
          <div>
            <nav>
              <div className="container">
                <div className="row">
                  <div className="col-auto my-auto pe-0">
                    <img
                      className="logo me-3"
                      style={{ width: "180px" }}
                      src={logo}
                      alt=""
                    />
                  </div>
                  <div className="col my-auto  d-flex justify-content-end">
                    <Button1
                      onClick={() => handleConnectWallet()}
                      label={
                        address
                          ? viewport != "mobile"
                            ? truncateAddress(address)
                            : truncateString(address, 6)
                          : `Connect ${viewport != "mobile" ? "Wallet" : ""}`
                      }
                      className={""}
                      iconName={undefined}
                      img={undefined}
                      imgClass={undefined}
                      style={
                        viewport != "mobile"
                          ? { color: "#2E100F" }
                          : { width: "150px", fontSize: "14px", color: "#2E100F" }
                      }
                      id={undefined}
                    />
                  </div>
                </div>
              </div>
            </nav>
            <div className="container">
              <div className="row">
                <div
                  className="col-12 text-center title1"
                  style={{ marginBottom: "24px" }}
                >
                  Swap
                </div>
                <div className="col-12 d-flex justify-content-center">
                  <div className="swapWrapper">
                    <div className="row">
                      <div className="col-12 mb-3">
                        <div className="row">
                          <div className="col-auto my-auto  pe-0">
                            <div className="dropdown">
                              <button
                                className="btn btn-secondary dropdown-toggle"
                                type="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                              >
                                <img
                                  src={fromToken.img}
                                  style={{
                                    borderRadius: "50%",
                                    width: "24px",
                                    height: "24px",
                                    marginTop: "2px",
                                    marginRight: "12px",
                                  }}
                                  className="tokenLogo"
                                  alt=""
                                />
                                {fromToken.name}
                              </button>
                              <ul className="dropdown-menu">
                                <li className="dropdown-item search d-flex align-items-center">
                                  <Icon name="search" className="me-2" />
                                  <input
                                    type="text"
                                    placeholder="Search"
                                    maxLength={10}
                                    value={searchTerm}
                                    onChange={(e) =>
                                      setSearchTerm(e.target.value)
                                    }
                                    className="form-control form-control-sm"
                                  />
                                </li>

                                <div className="list">
                                  <div className="list-inner">
                                    {filteredTokens.map((token, idx) => (
                                      <li
                                        key={idx}
                                        onClick={() => setFromToken(token)}
                                      >
                                        <span className="dropdown-item d-flex align-items-center">
                                          <img
                                            src={token.img}
                                            alt={token.name}
                                            className="tokenLogo"
                                            style={{
                                              borderRadius: "50%",
                                              width: "24px",
                                              marginTop: "-5px",
                                              marginRight: "8px",
                                            }}
                                          />
                                          {token.name}
                                        </span>
                                      </li>
                                    ))}
                                  </div>
                                </div>
                              </ul>
                            </div>
                          </div>
                          <div className="col my-auto d-flex justify-content-end title2">
                            12.000
                          </div>
                        </div>
                      </div>
                      <div className="col-12 mb-3">
                        <div className="row">
                          <div className="col-6 my-auto text1">
                            Balance:{" "}
                            {fromToken.balance ? fromToken.balance : "--"}
                          </div>
                          <div className="col-6 my-auto d-flex justify-content-end text2">
                            ~$20.95
                          </div>
                        </div>
                      </div>
                      <div className="col-12 mb-3 d-flex justify-content-center">
                        <div className="row w-100">
                          <div className="col p-0">
                            <Button1
                              onClick={() => setAmount("25%")}
                              label={"25%"}
                              className={`percentage first ${
                                amount === "25%" && "active"
                              }`}
                              iconName={undefined}
                              img={undefined}
                              imgClass={undefined}
                              style={undefined}
                              id={undefined}
                            />
                          </div>
                          <div className="col p-0">
                            <Button1
                              onClick={() => setAmount("50%")}
                              label={"50%"}
                              className={`percentage ${
                                amount === "50%" && "active"
                              }`}
                              iconName={undefined}
                              img={undefined}
                              imgClass={undefined}
                              style={undefined}
                              id={undefined}
                            />
                          </div>
                          <div className="col p-0">
                            <Button1
                              onClick={() => setAmount("75%")}
                              label={"75%"}
                              className={`percentage ${
                                amount === "75%" && "active"
                              }`}
                              iconName={undefined}
                              img={undefined}
                              imgClass={undefined}
                              style={undefined}
                              id={undefined}
                            />
                          </div>
                          <div className="col p-0">
                            <Button1
                              onClick={() => setAmount("100%")}
                              label={"100%"}
                              className={`percentage last ${
                                amount === "100%" && "active"
                              }`}
                              iconName={undefined}
                              img={undefined}
                              imgClass={undefined}
                              style={undefined}
                              id={undefined}
                            />
                          </div>
                        </div>
                      </div>
                      <div className="col-12 mb-3 mb-md-0 d-flex justify-content-center">
                        <Button1
                          onClick={() => handleSwap()}
                          label={""}
                          className={"swap"}
                          iconName={"swap"}
                          img={undefined}
                          imgClass={undefined}
                          style={undefined}
                          id={undefined}
                        />
                      </div>
                      <div className="col-12 mb-3">
                        <div className="row">
                          <div className="col-auto my-auto pe-0">
                            <div className="dropdown">
                              <button
                                className="btn btn-secondary dropdown-toggle"
                                type="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                              >
                                <img
                                  src={toToken.img}
                                  style={{
                                    borderRadius: "50%",
                                    width: "24px",
                                    height: "24px",
                                    marginTop: "2px",
                                    marginRight: "8px",
                                  }}
                                  className="tokenLogo"
                                  alt=""
                                />
                                {toToken.name}
                              </button>
                              <ul className="dropdown-menu">
                                <li className="dropdown-item search d-flex align-items-center">
                                  <Icon name="search" className="me-2" />
                                  <input
                                    type="text"
                                    placeholder="Search"
                                    maxLength={10}
                                    value={searchTerm}
                                    onChange={(e) =>
                                      setSearchTerm(e.target.value)
                                    }
                                    className="form-control form-control-sm"
                                  />
                                </li>

                                <div className="list">
                                  <div className="list-inner">
                                    {filteredTokens.map((token, idx) => (
                                      <li
                                        key={idx}
                                        onClick={() => setToToken(token)}
                                      >
                                        <span className="dropdown-item d-flex align-items-center">
                                          <img
                                            src={token.img}
                                            alt={token.name}
                                            className="tokenLogo"
                                            style={{
                                              borderRadius: "50%",
                                              width: "24px",
                                              marginTop: "-5px",
                                              marginRight: "12px",
                                            }}
                                          />
                                          {token.name}
                                        </span>
                                      </li>
                                    ))}
                                  </div>
                                </div>
                              </ul>
                            </div>
                          </div>
                          <div className="col my-auto d-flex justify-content-end title2">
                            20.9159
                          </div>
                        </div>
                      </div>
                      <div className="col-12 mb-3">
                        <div className="row">
                          <div className="col-6 my-auto text1">
                            Balance:{" "}
                            {toToken.balance ? toToken.balance : "--"}
                          </div>
                          <div className="col-6 my-auto d-flex justify-content-end text2">
                            <span className="textRed me-2">(-.16%)</span>{" "}
                            ~$20.95
                          </div>
                        </div>
                      </div>
                      <div className="col text2">
                        1ETH = 2.091.5949 USDC ≈ $2.094.77
                      </div>
                      <div className="col-auto d-flex justify-content-end text2 ">
                        <Icon name={"gas"} /> ~$0.01
                      </div>
                    </div>
                  </div>
                </div>
                <div className="col-12 text-center mt-4">
                  <Button1
                    onClick={() => handleFinishSwap()}
                    label={"Swap"}
                    className={""}
                    iconName={undefined}
                    img={undefined}
                    imgClass={undefined}
                    style={{ color: "#2E100F" }}
                    id={undefined}
                  />
                </div>
                {isRoute && (
                  <div className="col-12 d-flex justify-content-center">
                    <div className="accordion" id="route">
                      <div className="accordion-item">
                        <h2 className="accordion-header" id="headingOne">
                          <button
                            className={`accordion-button ${isRoute ? "" : "collapsed"}`}
                            type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#collapseOne"
                            aria-expanded={isRoute ? "true" : "false"}
                            aria-controls="collapseOne"
                          >
                            <div
                              className="row w-100 d-flex justify-content-between"
                              style={{ flexWrap: "nowrap" }}
                            >
                              <div className="col-auto">
                                <Icon
                                  name={"routeDropdown"}
                                  className="dropdownIcon"
                                />
                              </div>
                              <div className="col-auto text">
                                <Icon name={"route"} className="me-2" />
                                See Route
                              </div>
                              <div className="col-auto">
                                <Icon
                                  name={"routeDropdown"}
                                  className="dropdownIcon"
                                />
                              </div>
                            </div>
                          </button>
                        </h2>
                        <div
                          id="collapseOne"
                          className={`accordion-collapse collapse ${isRoute ? "show" : ""}`}
                          aria-labelledby="headingOne"
                          data-bs-parent="#route"
                        >
                          <div className="accordion-body">
                            {Object.keys(data1 || {}).length > 0 ? (
                              Object.entries(data1).map(([address, amount], index) => (
                                <div key={index} className="mb-2">
                                  {address}: {amount} <br />
                                </div>
                              ))
                            ) : (
                              <>
                                <div className="mb-2">Route 1: ETH → USDC → LINK</div>
                                <div className="mb-2">Route 2: ETH → LINK</div>
                                <div className="mb-2">Route 3: ETH → USDT → USDC</div>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
          <footer>
            <div className="row">
              <div className="col-12 text2 text-center d-flex justify-content-center">
                poweredby
              </div>
              <div className="col-12 d-flex justify-content-center">
                <img src={dalos} alt="" />
              </div>
            </div>
          </footer>
        </div>
      </section>
    </>
  );
}

export default App;
