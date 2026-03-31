import { ControlPlaneShell } from "@/components/control-plane-shell";
import { ExecutionPane } from "@/components/execution-pane";
import { StatusPanel } from "@/components/status-panel";
import { SystemGraphPanel } from "@/components/system-graph-panel";
import { VerificationStream } from "@/components/verification-stream";
import {
  loadStatusJson,
  loadSystemGraph,
  loadVerificationStream,
} from "@/lib/adapters";

/** Request-time reads of repo files; avoids serving only build-time snapshots of STATUS.json. */
export const dynamic = "force-dynamic";

export default async function HomePage() {
  const statusLoad = loadStatusJson();
  const systemGraphLoad = loadSystemGraph();
  const verificationLoad = loadVerificationStream();

  return (
    <ControlPlaneShell>
      <SystemGraphPanel load={systemGraphLoad} />
      <StatusPanel load={statusLoad} />
      <ExecutionPane statusLoad={statusLoad} />
      <VerificationStream load={verificationLoad} />
    </ControlPlaneShell>
  );
}
