const apiUrl = "https://opbento.edgexhq.tech/api/bento?n=Rohit%20Purkait&g=codeswithroh&x=codeswithroh001&l=codeswithroh&i=https%3A%2F%2Fmedia.licdn.com%2Fdms%2Fimage%2Fv2%2FD5603AQGK8QTsLa3-hg%2Fprofile-displayphoto-shrink_400_400%2FB56ZO7x58bGsAo-%2F0%2F1734022242960%3Fe%3D1741219200%26v%3Dbeta%26t%3DM_3Z5XoxSy_sfbaDWpnGuAc7EHb_Qob6zmZ6cq0GU3c&p=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fcodeswithroh%2F&z=ae433";
interface BentoResponse {
  url: string;
}

const fetchBentoUrl = async (apiUrl: string): Promise<string> => {
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: BentoResponse = (await response.json()) as BentoResponse;
    return data.url;
  } catch (error) {
    console.error("Error fetching Bento URL:", error);
    throw error;
  }
};

// @ts-ignore
fetchBentoUrl(apiUrl);
