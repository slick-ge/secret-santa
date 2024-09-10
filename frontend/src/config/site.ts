import { getBaseUrl } from "@/lib/utils";

export const siteConfig = {
  name: "Secret Santa",
  url: getBaseUrl(),
  links: {
    github: "https://github.com/ghvinerias/secret-santa",
  },
};

export type SiteConfig = typeof siteConfig;
