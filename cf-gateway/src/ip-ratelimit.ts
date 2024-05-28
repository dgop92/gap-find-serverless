const ipCountMap: { [key: string]: number } = {};

export enum RateLimitResponse {
	OK = 0,
	TOO_MANY_REQUESTS = 1,
	IP_NOT_FOUND = 2,
}

export function rateLimitByIp(request: Request, env: Env): RateLimitResponse {
	const ip = request.headers.get("cf-connecting-ip");

	if (!ip) {
		return RateLimitResponse.IP_NOT_FOUND;
	}

	// get ipcount or 0
	const count = ipCountMap[ip] || 0;

	console.log(`IP: ${ip} has ${count} requests`);

	if (count >= env.MAX_REQUESTS_PER_IP_PER_INSTANCE) {
		return RateLimitResponse.TOO_MANY_REQUESTS;
	}

	ipCountMap[ip] = count + 1;

	return RateLimitResponse.OK;
}
