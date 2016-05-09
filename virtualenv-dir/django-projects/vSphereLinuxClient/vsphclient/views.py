from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
import subprocess

def login(request):
    args = {}
    args.update(csrf(request)) 
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/vsphclient/index/', context_instance=RequestContext(request))
        else:
            args['login_error'] = "Invalid username or password."
            return render_to_response('login.html', args,  context_instance=RequestContext(request))
    else:
        return render_to_response('login.html', args,  context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return redirect('/vshclient/index/', context_instance=RequestContext(request))

def index(request):
#    getVirtMachines = subprocess.Popen("vmware-cmd --config /home/zinner/graduate-work/session.cfg -l", shell=True, stdout=subprocess.PIPE)
    getVirtMachines = subprocess.Popen("esxcli --config /home/zinner/graduate-work/session.cfg vm process list", shell=True, stdout=subprocess.PIPE)
    virtMachines = getVirtMachines.stdout.readlines()[0::8]
    return render_to_response(request, 'index.html', {'virt_machines': virtMachines, 'state': 'start'})

def home(request):
    return render_to_response(request, 'home.html', {})

def stopmachine(request):
    machine_id = request.POST['machine_id']
    cmd = "esxcli --config /home/zinner/graduate-work/session.cfg vm process kill -w %s -t soft" % machine_id
    stopMachine = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = stopMachine.stdout.readlines()
    print "result"
    print result
    print "id"
    print machine_id
    return render_to_response(request, 'index.html', {'result': result, 'state': 'stop'}) #, 'username': auth.get_user(request).username})
    #return render(request, 'index.html', {'result': result, 'state': 'stop'})
