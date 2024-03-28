package main

import (
	"fmt"
	"math"
)

const s string = "constant"
const c = "constant"

func main() {
	fmt.Println(s)
	fmt.Println(c)

	const n = 500000000

	const d = 3e20 / n
	fmt.Println(d)

	fmt.Println(int64(d))

	fmt.Println(math.Sin(n))
}
