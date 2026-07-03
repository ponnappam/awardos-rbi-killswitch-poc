package main
import ("encoding/json"; "fmt"; "log"; "net/http"; "os/exec"; "time")
type LoanRequest struct{Name string `json:"name"`; Income int `json:"income"`}
func killLLM()(float64,error){start:=time.Now();cmd:=exec.Command("docker","stop","balk-llm");err:=cmd.Run();return time.Since(start).Seconds(),err}
func handleLoan(w http.ResponseWriter,r *http.Request){var req LoanRequest;json.NewDecoder(r.Body).Decode(&req)
if req.Income>150000{latency,_:=killLLM();w.WriteHeader(200);json.NewEncoder(w).Encode(map[string]interface{}{"status":"KILLED","latency_s":latency,"reason":"MRMF 5.2"});return}
json.NewEncoder(w).Encode(map[string]string{"status":"APPROVED"})}
func main(){http.HandleFunc("/loan",handleLoan);fmt.Println("Awardos Gateway listening on :443");log.Fatal(http.ListenAndServeTLS(":443","/cert/cert.pem","/cert/key.pem",nil))}
