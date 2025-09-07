

export const aggregate = async (token1Address, token1Amount, token2Address) => {
  const url = "";

  const payload = {
    token1Address,
    token1Amount,
    token2Address,
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    return data
  } catch (error) {
    console.error("Hata:", error);
  }
};
