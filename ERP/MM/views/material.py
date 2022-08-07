
@login_required
def update_item(request: HttpRequest):
    pk = request.POST.get('pk')
    pk = str(int(pk)) # turn '002' into '2'
    material: Material = get_object_or_404(Material, pk=pk)
    form = MaterialForm(request.POST, instance=material)
    error_message = None

    if error_message is None:
        if form.is_valid():
            material.save()
            messages.success(request=request, message="Successfully updated!")
            return HttpResponseRedirect(reverse('MM:display_material', args=(material.pk,)))
        else:
            return render(
                request=request,
                template_name='../templates/material/material.html',
                context={'form': form, 'pk': int(pk)}
            )
    else:
        messages.error(request=request, message=error_message)
        return HttpResponseRedirect(reverse('MM:display_material', args=(material.pk,)))

@login_required
def search_item(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/material/search_material.html'
        )
    elif request.method == 'POST':
        post = request.POST
        pk = getPk(post.get('pk'))
        mname = getRegex(post.get('mname'))
        mType = getRegex(post.get('mType'))
        industrySector = getRegex(post.get('industrySector'))
        materials = Material.objects.filter(
            pk__regex=pk, mname__regex=mname, mType__regex=mType, industrySector__regex=industrySector
        )
        
        if len(materials) > 0:
            messages.success(request=request, message="Succeed to get {:} results.".format(len(materials)))
            return render(
                request=request,
                template_name='../templates/material/search_material.html',
                context={'materials':materials}
            )
        else:
            messages.success(request=request, message="There is no matched result.")
            return render(
                request=request,
                template_name='../templates/material/search_material.html',
            )